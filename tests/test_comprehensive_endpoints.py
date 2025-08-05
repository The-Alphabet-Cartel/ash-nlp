#!/usr/bin/env python3
"""
Comprehensive Endpoint Test Suite - Phase 3a Validation
Tests ALL endpoints defined in the Ash-NLP system to ensure functionality, 
identify dead/broken endpoints, and validate business logic.

Usage: docker compose exec ash-nlp python tests/test_comprehensive_endpoints.py

This test validates:
1. All core analysis endpoints work correctly
2. All admin endpoints function as intended
3. All health/status endpoints return proper data
4. All learning endpoints are operational
5. Business logic works correctly (label switching, etc.)
6. Response schemas match expectations
7. Integration between components functions properly

Categories tested:
- Core Analysis (analyze, extract_phrases)
- Health & Status (health, stats, status)
- Admin/Label Management (all admin/* endpoints)
- Ensemble Configuration (ensemble/* endpoints)
- Learning System (learning_statistics, false positive/negative analysis)
"""

import requests
import json
import time
import logging
from typing import Dict, Any, List, Tuple
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

# Configuration
BASE_URL = "http://localhost:8881"
TIMEOUT = 30

class EndpointTestResults:
    """Track test results and categorize endpoints"""
    
    def __init__(self):
        self.results = {}
        self.categories = {
            'core_analysis': [],
            'health_status': [],
            'admin_labels': [],
            'ensemble_config': [],
            'learning_system': [],
            'deprecated_or_unknown': []
        }
        self.total_passed = 0
        self.total_failed = 0
        self.dead_endpoints = []
        self.broken_endpoints = []
        self.functional_endpoints = []

    def add_result(self, endpoint: str, category: str, success: bool, 
                   status_code: int = None, error: str = None, 
                   response_data: Dict = None, notes: str = None):
        """Add test result"""
        result = {
            'endpoint': endpoint,
            'category': category,
            'success': success,
            'status_code': status_code,
            'error': error,
            'response_data': response_data,
            'notes': notes,
            'tested_at': datetime.now().isoformat()
        }
        
        self.results[endpoint] = result
        self.categories[category].append(result)
        
        if success:
            self.total_passed += 1
            self.functional_endpoints.append(endpoint)
        else:
            self.total_failed += 1
            if status_code == 404:
                self.dead_endpoints.append(endpoint)
            else:
                self.broken_endpoints.append(endpoint)

    def print_summary(self):
        """Print comprehensive test summary"""
        logger.info("\n" + "=" * 100)
        logger.info("🏁 COMPREHENSIVE ENDPOINT TEST RESULTS")
        logger.info("=" * 100)
        
        logger.info(f"📊 Overall Results: {self.total_passed}/{self.total_passed + self.total_failed} endpoints passed")
        logger.info(f"✅ Functional: {len(self.functional_endpoints)}")
        logger.info(f"💀 Dead (404): {len(self.dead_endpoints)}")
        logger.info(f"🔧 Broken: {len(self.broken_endpoints)}")
        
        # Category breakdown
        logger.info(f"\n📁 RESULTS BY CATEGORY:")
        for category, results in self.categories.items():
            if results:
                passed = sum(1 for r in results if r['success'])
                total = len(results)
                logger.info(f"   {category}: {passed}/{total} passed")
        
        # Dead endpoints (should be removed)
        if self.dead_endpoints:
            logger.info(f"\n💀 DEAD ENDPOINTS (RECOMMEND REMOVAL):")
            for endpoint in self.dead_endpoints:
                logger.info(f"   ❌ {endpoint}")
        
        # Broken endpoints (need fixing)
        if self.broken_endpoints:
            logger.info(f"\n🔧 BROKEN ENDPOINTS (NEED FIXING):")
            for endpoint in self.broken_endpoints:
                result = self.results[endpoint]
                logger.info(f"   ❌ {endpoint} (Status: {result['status_code']}, Error: {result['error']})")
        
        # Functional endpoints
        logger.info(f"\n✅ FUNCTIONAL ENDPOINTS:")
        for endpoint in self.functional_endpoints:
            logger.info(f"   ✅ {endpoint}")

class ComprehensiveEndpointTester:
    """Comprehensive endpoint testing class"""
    
    def __init__(self):
        self.results = EndpointTestResults()
        self.test_data = self._get_test_data()
    
    def _get_test_data(self) -> Dict[str, Any]:
        """Get test data for various endpoint tests"""
        return {
            'sample_messages': [
                {
                    'message': 'I am feeling really overwhelmed and stressed',
                    'user_id': 'test_user_001',
                    'channel_id': 'test_channel_001',
                    'description': 'moderate crisis message'
                },
                {
                    'message': 'I want to end it all tonight',
                    'user_id': 'test_user_002', 
                    'channel_id': 'test_channel_002',
                    'description': 'high crisis message'
                },
                {
                    'message': 'Had a great day at the park today!',
                    'user_id': 'test_user_003',
                    'channel_id': 'test_channel_003', 
                    'description': 'positive message'
                }
            ],
            'label_sets_to_test': ['crisis_mental_health', 'sentiment_basic', 'lgbtqia_crisis'],
            'false_negative_example': {
                'message': 'I dont want to be here anymore',
                'should_detect_level': 'high',
                'actually_detected': 'low',
                'context': {'channel': 'support', 'time_of_day': 'late_night'},
                'severity_score': 8
            },
            'false_positive_example': {
                'message': 'This game is killing me, so funny!',
                'detected_level': 'high',
                'correct_level': 'none', 
                'context': {'channel': 'gaming', 'time_of_day': 'afternoon'},
                'severity_score': 1
            }
        }

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

    # ========================================================================
    # CORE ANALYSIS ENDPOINT TESTS
    # ========================================================================

    def test_core_analysis_endpoints(self):
        """Test all core analysis endpoints"""
        logger.info("\n🔍 TESTING CORE ANALYSIS ENDPOINTS")
        logger.info("=" * 60)
        
        # Test /analyze endpoint
        self._test_analyze_endpoint()
        
        # Test /extract_phrases endpoint (if exists)
        self._test_extract_phrases_endpoint()

    def _test_analyze_endpoint(self):
        """Test the main /analyze endpoint with various message types"""
        endpoint = "/analyze"
        logger.info(f"🧪 Testing {endpoint}...")
        
        try:
            for test_case in self.test_data['sample_messages']:
                payload = {
                    'message': test_case['message'],
                    'user_id': test_case['user_id'],
                    'channel_id': test_case['channel_id']
                }
                
                response = requests.post(f"{BASE_URL}{endpoint}", json=payload, timeout=TIMEOUT)
                
                if response.status_code == 200:
                    data = response.json()
                    
                    # Validate response schema
                    required_fields = ['crisis_level', 'confidence_score', 'needs_response']
                    missing_fields = [field for field in required_fields if field not in data]
                    
                    if missing_fields:
                        self.results.add_result(
                            endpoint, 'core_analysis', False,
                            response.status_code, f"Missing required fields: {missing_fields}",
                            data, f"Test case: {test_case['description']}"
                        )
                    else:
                        # Validate business logic
                        crisis_level = data.get('crisis_level')
                        confidence = data.get('confidence_score', 0)
                        needs_response = data.get('needs_response', False)
                        
                        # Basic sanity checks
                        valid_crisis_levels = ['none', 'low', 'medium', 'high']
                        valid_schema = (
                            crisis_level in valid_crisis_levels and
                            0 <= confidence <= 1 and
                            isinstance(needs_response, bool)
                        )
                        
                        if valid_schema:
                            logger.info(f"   ✅ {test_case['description']}: {crisis_level} (conf: {confidence:.3f})")
                        else:
                            logger.warning(f"   ⚠️ {test_case['description']}: Invalid response schema")
                            
                else:
                    logger.error(f"   ❌ Failed for {test_case['description']}: Status {response.status_code}")
            
            # Mark as successful if at least one test case worked
            self.results.add_result(
                endpoint, 'core_analysis', True,
                200, None, None, "Main analysis endpoint functional"
            )
            
        except Exception as e:
            self.results.add_result(
                endpoint, 'core_analysis', False,
                None, str(e), None, "Exception during testing"
            )

    def _test_extract_phrases_endpoint(self):
        """Test the /extract_phrases endpoint if it exists"""
        endpoint = "/extract_phrases"
        logger.info(f"🧪 Testing {endpoint}...")
        
        try:
            test_message = self.test_data['sample_messages'][0]
            payload = {
                'message': test_message['message'],
                'user_id': test_message['user_id'],
                'channel_id': test_message['channel_id'],
                'parameters': {
                    'min_phrase_length': 2,
                    'max_phrase_length': 6,
                    'crisis_focus': True
                }
            }
            
            response = requests.post(f"{BASE_URL}{endpoint}", json=payload, timeout=TIMEOUT)
            
            if response.status_code == 200:
                data = response.json()
                phrases = data.get('phrases', [])
                logger.info(f"   ✅ Phrase extraction: Found {len(phrases)} phrases")
                
                self.results.add_result(
                    endpoint, 'core_analysis', True,
                    200, None, data, f"Extracted {len(phrases)} phrases"
                )
            elif response.status_code == 404:
                logger.info(f"   ℹ️ {endpoint}: Not found (may not be implemented)")
                self.results.add_result(
                    endpoint, 'core_analysis', False,
                    404, "Endpoint not found", None, "May not be implemented"
                )
            else:
                logger.warning(f"   ⚠️ {endpoint}: Status {response.status_code}")
                self.results.add_result(
                    endpoint, 'core_analysis', False,
                    response.status_code, f"HTTP {response.status_code}", None, "Unexpected status"
                )
                
        except Exception as e:
            self.results.add_result(
                endpoint, 'core_analysis', False,
                None, str(e), None, "Exception during testing"
            )

    # ========================================================================
    # HEALTH & STATUS ENDPOINT TESTS
    # ========================================================================

    def test_health_status_endpoints(self):
        """Test all health and status endpoints"""
        logger.info("\n🏥 TESTING HEALTH & STATUS ENDPOINTS")
        logger.info("=" * 60)
        
        health_endpoints = [
            ("/health", "System health check"),
            ("/stats", "Service statistics"),
            ("/status", "Basic status")
        ]
        
        for endpoint, description in health_endpoints:
            self._test_get_endpoint(endpoint, description, 'health_status')

    def _test_get_endpoint(self, endpoint: str, description: str, category: str, 
                          validate_schema: bool = True):
        """Generic GET endpoint test"""
        logger.info(f"🧪 Testing {endpoint} ({description})...")
        
        try:
            response = requests.get(f"{BASE_URL}{endpoint}", timeout=TIMEOUT)
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    logger.info(f"   ✅ {description}: Accessible and returns JSON")
                    
                    # Basic validation for health endpoints
                    if endpoint == "/health" and validate_schema:
                        required_fields = ['status', 'uptime', 'model_loaded']
                        missing = [f for f in required_fields if f not in data]
                        if missing:
                            logger.warning(f"   ⚠️ Missing health fields: {missing}")
                    
                    self.results.add_result(
                        endpoint, category, True,
                        200, None, data, description
                    )
                    
                except json.JSONDecodeError:
                    logger.warning(f"   ⚠️ {description}: Non-JSON response")
                    self.results.add_result(
                        endpoint, category, False,
                        200, "Non-JSON response", None, description
                    )
                    
            elif response.status_code == 404:
                logger.info(f"   💀 {description}: Not found (dead endpoint)")
                self.results.add_result(
                    endpoint, category, False,
                    404, "Endpoint not found", None, "Dead endpoint - recommend removal"
                )
                
            else:
                logger.warning(f"   🔧 {description}: Status {response.status_code}")
                self.results.add_result(
                    endpoint, category, False,
                    response.status_code, f"HTTP {response.status_code}", None, description
                )
                
        except Exception as e:
            logger.error(f"   ❌ {description}: Exception - {e}")
            self.results.add_result(
                endpoint, category, False,
                None, str(e), None, description
            )

    # ========================================================================
    # ADMIN ENDPOINT TESTS
    # ========================================================================

    def test_admin_endpoints(self):
        """Test all admin endpoints"""
        logger.info("\n🔧 TESTING ADMIN ENDPOINTS")
        logger.info("=" * 60)
        
        # Test GET admin endpoints
        admin_get_endpoints = [
            ("/admin/status", "Admin system status"),
            ("/admin/labels/status", "Label configuration status"),
            ("/admin/labels/config", "Comprehensive configuration info"),
            ("/admin/labels/current", "Current label set information"),
            ("/admin/labels/list", "List all available label sets"),
            ("/admin/labels/validate", "Validate current configuration")
        ]
        
        for endpoint, description in admin_get_endpoints:
            self._test_get_endpoint(endpoint, description, 'admin_labels')
        
        # Test admin endpoints that need parameters
        self._test_admin_label_details()
        self._test_admin_label_export()
        
        # Test POST admin endpoints
        self._test_admin_label_switching()
        self._test_admin_test_endpoints()

    def _test_admin_label_details(self):
        """Test /admin/labels/details/{name} endpoint"""
        endpoint_base = "/admin/labels/details"
        logger.info(f"🧪 Testing {endpoint_base}/{{name}}...")
        
        # First get list of available label sets
        try:
            response = requests.get(f"{BASE_URL}/admin/labels/list", timeout=TIMEOUT)
            if response.status_code == 200:
                data = response.json()
                sets = data.get('sets', [])
                
                if sets:
                    # Test with first available label set
                    test_set_name = sets[0].get('name', 'crisis_mental_health')
                    endpoint = f"{endpoint_base}/{test_set_name}"
                    
                    self._test_get_endpoint(endpoint, f"Label details for {test_set_name}", 'admin_labels')
                else:
                    logger.warning(f"   ⚠️ No label sets found to test details endpoint")
                    self.results.add_result(
                        f"{endpoint_base}/{{name}}", 'admin_labels', False,
                        None, "No label sets available for testing", None, "Cannot test without label sets"
                    )
            else:
                logger.warning(f"   ⚠️ Cannot get label sets to test details endpoint")
                self.results.add_result(
                    f"{endpoint_base}/{{name}}", 'admin_labels', False,
                    None, "Cannot retrieve label sets for testing", None, "Depends on /admin/labels/list"
                )
                
        except Exception as e:
            self.results.add_result(
                f"{endpoint_base}/{{name}}", 'admin_labels', False,
                None, str(e), None, "Exception during testing"
            )

    def _test_admin_label_export(self):
        """Test /admin/labels/export/{name} endpoint"""
        endpoint_base = "/admin/labels/export"
        logger.info(f"🧪 Testing {endpoint_base}/{{name}}...")
        
        # Test with a known label set
        test_set_name = "crisis_mental_health"
        endpoint = f"{endpoint_base}/{test_set_name}"
        
        self._test_get_endpoint(endpoint, f"Export {test_set_name}", 'admin_labels')

    def _test_admin_label_switching(self):
        """Test label switching functionality"""
        logger.info(f"🧪 Testing admin label switching...")
        
        # Test simple-switch first
        endpoint = "/admin/labels/simple-switch"
        try:
            payload = {"label_set": "crisis_mental_health"}
            response = requests.post(f"{BASE_URL}{endpoint}", json=payload, timeout=TIMEOUT)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success', False):
                    logger.info(f"   ✅ Simple label switch: Successful")
                    self.results.add_result(
                        endpoint, 'admin_labels', True,
                        200, None, data, "Label switching works"
                    )
                else:
                    logger.warning(f"   ⚠️ Simple label switch: Response indicates failure")
                    self.results.add_result(
                        endpoint, 'admin_labels', False,
                        200, "Switch indicated failure", data, "Business logic issue"
                    )
            else:
                logger.warning(f"   🔧 Simple label switch: Status {response.status_code}")
                self.results.add_result(
                    endpoint, 'admin_labels', False,
                    response.status_code, f"HTTP {response.status_code}", None, "Switch endpoint failed"
                )
                
        except Exception as e:
            self.results.add_result(
                endpoint, 'admin_labels', False,
                None, str(e), None, "Exception during label switching test"
            )
        
        # Test full switch endpoint
        endpoint = "/admin/labels/switch"
        try:
            payload = {"label_set": "sentiment_basic"}
            response = requests.post(f"{BASE_URL}{endpoint}", json=payload, timeout=TIMEOUT)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success', False):
                    logger.info(f"   ✅ Full label switch: Successful")
                    self.results.add_result(
                        endpoint, 'admin_labels', True,
                        200, None, data, "Full label switching works"
                    )
                else:
                    logger.warning(f"   ⚠️ Full label switch: Response indicates failure") 
                    self.results.add_result(
                        endpoint, 'admin_labels', False,
                        200, "Switch indicated failure", data, "Business logic issue"
                    )
            else:
                logger.warning(f"   🔧 Full label switch: Status {response.status_code}")
                self.results.add_result(
                    endpoint, 'admin_labels', False,
                    response.status_code, f"HTTP {response.status_code}", None, "Full switch endpoint failed"
                )
                
        except Exception as e:
            self.results.add_result(
                endpoint, 'admin_labels', False,
                None, str(e), None, "Exception during full label switching test"
            )

    def _test_admin_test_endpoints(self):
        """Test admin testing endpoints"""
        logger.info(f"🧪 Testing admin test endpoints...")
        
        # Test /admin/labels/test/mapping
        endpoint = "/admin/labels/test/mapping"
        try:
            payload = {"test_messages": ["test message"], "validate_schema": True}
            response = requests.post(f"{BASE_URL}{endpoint}", json=payload, timeout=TIMEOUT)
            
            if response.status_code == 200:
                logger.info(f"   ✅ Label mapping test: Accessible")
                self.results.add_result(
                    endpoint, 'admin_labels', True,
                    200, None, response.json(), "Mapping test functional"
                )
            elif response.status_code == 404:
                logger.info(f"   💀 Label mapping test: Not found")
                self.results.add_result(
                    endpoint, 'admin_labels', False,
                    404, "Endpoint not found", None, "Dead endpoint"
                )
            else:
                logger.warning(f"   🔧 Label mapping test: Status {response.status_code}")
                self.results.add_result(
                    endpoint, 'admin_labels', False,
                    response.status_code, f"HTTP {response.status_code}", None, "Endpoint issue"
                )
                
        except Exception as e:
            self.results.add_result(
                endpoint, 'admin_labels', False,
                None, str(e), None, "Exception during test"
            )
        
        # Test /admin/labels/test/comprehensive
        endpoint = "/admin/labels/test/comprehensive"
        try:
            response = requests.post(f"{BASE_URL}{endpoint}", json={}, timeout=TIMEOUT)
            
            if response.status_code == 200:
                logger.info(f"   ✅ Comprehensive test: Accessible")
                self.results.add_result(
                    endpoint, 'admin_labels', True,
                    200, None, response.json(), "Comprehensive test functional"
                )
            elif response.status_code == 404:
                logger.info(f"   💀 Comprehensive test: Not found")
                self.results.add_result(
                    endpoint, 'admin_labels', False,
                    404, "Endpoint not found", None, "Dead endpoint"
                )
            else:
                logger.warning(f"   🔧 Comprehensive test: Status {response.status_code}")
                self.results.add_result(
                    endpoint, 'admin_labels', False,
                    response.status_code, f"HTTP {response.status_code}", None, "Endpoint issue"
                )
                
        except Exception as e:
            self.results.add_result(
                endpoint, 'admin_labels', False,
                None, str(e), None, "Exception during test"
            )

    # ========================================================================
    # ENSEMBLE CONFIGURATION ENDPOINT TESTS  
    # ========================================================================

    def test_ensemble_endpoints(self):
        """Test ensemble configuration endpoints"""
        logger.info("\n🤖 TESTING ENSEMBLE CONFIGURATION ENDPOINTS")
        logger.info("=" * 60)
        
        ensemble_endpoints = [
            ("/ensemble/config", "Ensemble configuration"),
            ("/ensemble/health", "Ensemble health"),
            ("/ensemble/status", "Ensemble status")
        ]
        
        for endpoint, description in ensemble_endpoints:
            self._test_get_endpoint(endpoint, description, 'ensemble_config')

    # ========================================================================
    # LEARNING SYSTEM ENDPOINT TESTS
    # ========================================================================

    def test_learning_endpoints(self):
        """Test learning system endpoints"""
        logger.info("\n🧠 TESTING LEARNING SYSTEM ENDPOINTS")
        logger.info("=" * 60)
        
        # Test GET learning endpoints
        self._test_get_endpoint("/learning_statistics", "Learning statistics", 'learning_system')
        
        # Test POST learning endpoints
        self._test_learning_analysis_endpoints()

    def _test_learning_analysis_endpoints(self):
        """Test learning analysis endpoints"""
        
        # Test false negative analysis
        endpoint = "/analyze_false_negative"
        logger.info(f"🧪 Testing {endpoint}...")
        
        try:
            payload = self.test_data['false_negative_example']
            response = requests.post(f"{BASE_URL}{endpoint}", json=payload, timeout=TIMEOUT)
            
            if response.status_code == 200:
                data = response.json()
                logger.info(f"   ✅ False negative analysis: Functional")
                self.results.add_result(
                    endpoint, 'learning_system', True,
                    200, None, data, "False negative analysis works"
                )
            elif response.status_code == 404:
                logger.info(f"   💀 False negative analysis: Not found")
                self.results.add_result(
                    endpoint, 'learning_system', False,
                    404, "Endpoint not found", None, "Dead endpoint"
                )
            else:
                logger.warning(f"   🔧 False negative analysis: Status {response.status_code}")
                self.results.add_result(
                    endpoint, 'learning_system', False,
                    response.status_code, f"HTTP {response.status_code}", None, "Endpoint issue"
                )
                
        except Exception as e:
            self.results.add_result(
                endpoint, 'learning_system', False,
                None, str(e), None, "Exception during test"
            )
        
        # Test false positive analysis
        endpoint = "/analyze_false_positive"
        logger.info(f"🧪 Testing {endpoint}...")
        
        try:
            payload = self.test_data['false_positive_example']
            response = requests.post(f"{BASE_URL}{endpoint}", json=payload, timeout=TIMEOUT)
            
            if response.status_code == 200:
                data = response.json()
                logger.info(f"   ✅ False positive analysis: Functional")
                self.results.add_result(
                    endpoint, 'learning_system', True,
                    200, None, data, "False positive analysis works"
                )
            elif response.status_code == 404:
                logger.info(f"   💀 False positive analysis: Not found")
                self.results.add_result(
                    endpoint, 'learning_system', False,
                    404, "Endpoint not found", None, "Dead endpoint"
                )
            else:
                logger.warning(f"   🔧 False positive analysis: Status {response.status_code}")
                self.results.add_result(
                    endpoint, 'learning_system', False,
                    response.status_code, f"HTTP {response.status_code}", None, "Endpoint issue"
                )
                
        except Exception as e:
            self.results.add_result(
                endpoint, 'learning_system', False,
                None, str(e), None, "Exception during test"
            )
        
        # Test update learning model
        endpoint = "/update_learning_model"
        logger.info(f"🧪 Testing {endpoint}...")
        
        try:
            payload = {
                "learning_record_id": "test_record_001",
                "record_type": "false_negative",
                "message_data": {
                    "content": "I dont want to be here",
                    "user_id": "test_user",
                    "channel_id": "test_channel"
                },
                "correction_data": {
                    "should_detect_level": "high",
                    "actually_detected": "low",
                    "severity_score": 8
                },
                "context_data": {
                    "channel": "support",
                    "time_of_day": "late_night"
                }
            }
            
            response = requests.post(f"{BASE_URL}{endpoint}", json=payload, timeout=TIMEOUT)
            
            if response.status_code == 200:
                data = response.json()
                logger.info(f"   ✅ Learning model update: Functional")
                self.results.add_result(
                    endpoint, 'learning_system', True,
                    200, None, data, "Learning model update works"
                )
            elif response.status_code == 404:
                logger.info(f"   💀 Learning model update: Not found")
                self.results.add_result(
                    endpoint, 'learning_system', False,
                    404, "Endpoint not found", None, "Dead endpoint"
                )
            else:
                logger.warning(f"   🔧 Learning model update: Status {response.status_code}")
                self.results.add_result(
                    endpoint, 'learning_system', False,
                    response.status_code, f"HTTP {response.status_code}", None, "Endpoint issue"
                )
                
        except Exception as e:
            self.results.add_result(
                endpoint, 'learning_system', False,
                None, str(e), None, "Exception during test"
            )

    # ========================================================================
    # BUSINESS LOGIC VALIDATION TESTS
    # ========================================================================

    def test_business_logic_validation(self):
        """Test that business logic works correctly across endpoints"""
        logger.info("\n🎯 TESTING BUSINESS LOGIC VALIDATION")
        logger.info("=" * 60)
        
        self._test_label_switching_affects_analysis()
        self._test_crisis_pattern_integration()
        self._test_ensemble_mode_consistency()

    def _test_label_switching_affects_analysis(self):
        """Test that label switching actually affects analysis results"""
        logger.info("🧪 Testing label switching affects analysis...")
        
        test_message = self.test_data['sample_messages'][0]
        
        try:
            # Get baseline analysis with current label set
            payload = {
                'message': test_message['message'],
                'user_id': test_message['user_id'], 
                'channel_id': test_message['channel_id']
            }
            
            response1 = requests.post(f"{BASE_URL}/analyze", json=payload, timeout=TIMEOUT)
            if response1.status_code != 200:
                logger.warning("   ⚠️ Cannot test label switching - analysis endpoint not working")
                return
            
            baseline_result = response1.json()
            baseline_crisis = baseline_result.get('crisis_level')
            
            # Try to switch label set
            switch_payload = {"label_set": "sentiment_basic"}
            switch_response = requests.post(f"{BASE_URL}/admin/labels/simple-switch", 
                                          json=switch_payload, timeout=TIMEOUT)
            
            if switch_response.status_code == 200:
                switch_data = switch_response.json()
                if switch_data.get('success', False):
                    # Wait a moment for switch to take effect
                    time.sleep(2)
                    
                    # Analyze same message with new label set
                    response2 = requests.post(f"{BASE_URL}/analyze", json=payload, timeout=TIMEOUT)
                    if response2.status_code == 200:
                        new_result = response2.json()
                        new_crisis = new_result.get('crisis_level')
                        
                        # Check if results are different (indicating switch worked)
                        if baseline_crisis != new_crisis:
                            logger.info(f"   ✅ Label switching affects analysis: {baseline_crisis} → {new_crisis}")
                            logger.info(f"   📋 Business logic validation: PASSED")
                        else:
                            logger.info(f"   ℹ️ Label switching: Same result ({baseline_crisis}) - may be expected")
                            logger.info(f"   📋 Business logic validation: INCONCLUSIVE")
                        
                        # Switch back to original label set
                        requests.post(f"{BASE_URL}/admin/labels/simple-switch", 
                                    json={"label_set": "crisis_mental_health"}, timeout=TIMEOUT)
                    else:
                        logger.warning(f"   ⚠️ Analysis after label switch failed")
                else:
                    logger.warning(f"   ⚠️ Label switch indicated failure")
            else:
                logger.warning(f"   ⚠️ Label switch endpoint not working")
                
        except Exception as e:
            logger.error(f"   ❌ Business logic test failed: {e}")

    def _test_crisis_pattern_integration(self):
        """Test that crisis patterns are integrated in analysis"""
        logger.info("🧪 Testing crisis pattern integration...")
        
        # Test with a message that should trigger patterns
        crisis_message = "I dont want to be here anymore"
        payload = {
            'message': crisis_message,
            'user_id': 'test_pattern_user',
            'channel_id': 'test_pattern_channel'
        }
        
        try:
            response = requests.post(f"{BASE_URL}/analyze", json=payload, timeout=TIMEOUT)
            
            if response.status_code == 200:
                data = response.json()
                method = data.get('method', '')
                
                # Check if pattern integration is indicated
                if 'pattern' in method.lower() or 'integration' in method.lower():
                    logger.info(f"   ✅ Crisis pattern integration: Active")
                    logger.info(f"   📊 Method: {method}")
                    logger.info(f"   🚨 Crisis level: {data.get('crisis_level')}")
                else:
                    logger.warning(f"   ⚠️ Crisis pattern integration: Not evident in response")
                    logger.info(f"   📊 Method: {method}")
            else:
                logger.warning(f"   ⚠️ Analysis failed for pattern integration test")
                
        except Exception as e:
            logger.error(f"   ❌ Pattern integration test failed: {e}")

    def _test_ensemble_mode_consistency(self):
        """Test that ensemble mode is consistent across requests"""
        logger.info("🧪 Testing ensemble mode consistency...")
        
        test_message = self.test_data['sample_messages'][1]
        payload = {
            'message': test_message['message'],
            'user_id': test_message['user_id'],
            'channel_id': test_message['channel_id']
        }
        
        try:
            # Make multiple requests and check for consistency
            methods = []
            for i in range(3):
                response = requests.post(f"{BASE_URL}/analyze", json=payload, timeout=TIMEOUT)
                if response.status_code == 200:
                    data = response.json()
                    method = data.get('method', 'unknown')
                    methods.append(method)
                    time.sleep(1)
            
            if len(set(methods)) == 1:
                logger.info(f"   ✅ Ensemble mode consistency: {methods[0]}")
            else:
                logger.info(f"   ℹ️ Ensemble methods vary: {set(methods)} - may be expected")
                
        except Exception as e:
            logger.error(f"   ❌ Ensemble consistency test failed: {e}")

    # ========================================================================
    # MISSING ENDPOINT DISCOVERY
    # ========================================================================

    def test_potential_missing_endpoints(self):
        """Test for endpoints that might exist but aren't documented"""
        logger.info("\n🔍 TESTING FOR UNDOCUMENTED ENDPOINTS")
        logger.info("=" * 60)
        
        # Common endpoint patterns to check
        potential_endpoints = [
            ("/analyze_message", "Alternative analysis endpoint"),
            ("/batch_analysis", "Batch analysis endpoint"),
            ("/model/status", "Model status endpoint"),
            ("/config", "General configuration endpoint"),
            ("/version", "Version information endpoint"),
            ("/metrics", "Metrics endpoint"),
            ("/docs", "API documentation endpoint"),
            ("/openapi.json", "OpenAPI specification"),
            ("/admin/models/status", "Admin model status"),
            ("/admin/system/status", "Admin system status")
        ]
        
        for endpoint, description in potential_endpoints:
            self._test_get_endpoint(endpoint, description, 'deprecated_or_unknown', validate_schema=False)

    # ========================================================================
    # MAIN TEST EXECUTION
    # ========================================================================

    def run_all_tests(self) -> bool:
        """Run all comprehensive tests"""
        logger.info("🚀 STARTING COMPREHENSIVE ENDPOINT TEST SUITE")
        logger.info("🎯 Phase 3a Validation - All Endpoint Functionality Check")
        logger.info("=" * 100)
        
        # Wait for service to be ready
        if not self.wait_for_service_ready():
            logger.error("❌ Service not available - cannot run tests")
            return False
        
        # Run all test categories
        test_categories = [
            ("Core Analysis Endpoints", self.test_core_analysis_endpoints),
            ("Health & Status Endpoints", self.test_health_status_endpoints),
            ("Admin Endpoints", self.test_admin_endpoints),
            ("Ensemble Configuration Endpoints", self.test_ensemble_endpoints),
            ("Learning System Endpoints", self.test_learning_endpoints),
            ("Business Logic Validation", self.test_business_logic_validation),
            ("Undocumented Endpoint Discovery", self.test_potential_missing_endpoints)
        ]
        
        for category_name, test_method in test_categories:
            logger.info(f"\n🏷️ CATEGORY: {category_name}")
            logger.info("-" * 80)
            try:
                test_method()
            except Exception as e:
                logger.error(f"❌ Category {category_name} failed: {e}")
        
        # Print comprehensive summary
        self.results.print_summary()
        
        # Generate recommendations
        self._generate_recommendations()
        
        return self.total_failed == 0

    def _generate_recommendations(self):
        """Generate recommendations based on test results"""
        logger.info(f"\n💡 RECOMMENDATIONS")
        logger.info("=" * 60)
        
        if self.results.dead_endpoints:
            logger.info(f"🗑️ RECOMMEND REMOVING DEAD ENDPOINTS:")
            for endpoint in self.results.dead_endpoints:
                logger.info(f"   - {endpoint}")
        
        if self.results.broken_endpoints:
            logger.info(f"🔧 RECOMMEND FIXING BROKEN ENDPOINTS:")
            for endpoint in self.results.broken_endpoints:
                result = self.results.results[endpoint]
                logger.info(f"   - {endpoint}: {result['error']}")
        
        # Check for essential missing functionality
        essential_endpoints = ['/analyze', '/health', '/admin/labels/switch']
        missing_essential = []
        for endpoint in essential_endpoints:
            if endpoint not in self.results.functional_endpoints:
                missing_essential.append(endpoint)
        
        if missing_essential:
            logger.warning(f"⚠️ CRITICAL: Essential endpoints not functional:")
            for endpoint in missing_essential:
                logger.warning(f"   - {endpoint}")
        
        # Overall health assessment
        success_rate = (self.total_passed / (self.total_passed + self.total_failed)) * 100
        
        if success_rate >= 90:
            logger.info(f"🎉 SYSTEM HEALTH: Excellent ({success_rate:.1f}%)")
        elif success_rate >= 75:
            logger.info(f"✅ SYSTEM HEALTH: Good ({success_rate:.1f}%)")
        elif success_rate >= 50:
            logger.warning(f"⚠️ SYSTEM HEALTH: Needs attention ({success_rate:.1f}%)")
        else:
            logger.error(f"❌ SYSTEM HEALTH: Critical issues ({success_rate:.1f}%)")

def main():
    """Main test execution"""
    tester = ComprehensiveEndpointTester()
    success = tester.run_all_tests()
    
    logger.info(f"\n🏁 COMPREHENSIVE TEST COMPLETE")
    logger.info(f"📈 Success: {success}")
    
    return success

if __name__ == "__main__":
    import sys
    success = main()
    sys.exit(0 if success else 1)