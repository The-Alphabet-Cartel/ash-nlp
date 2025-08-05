#!/usr/bin/env python3
"""
Endpoint Discovery and Cleanup Analysis
Discovers all endpoints, categorizes them, and provides cleanup recommendations.

Usage: docker compose exec ash-nlp python tests/test_endpoint_discovery.py

This script:
1. Tests every endpoint we know about from the codebase
2. Discovers any endpoints we might have missed
3. Categorizes endpoints by functionality and importance
4. Provides specific recommendations for cleanup
5. Identifies truly dead code vs temporarily broken endpoints
"""

import requests
import json
import time
import logging
from typing import Dict, Any, List, Set, Optional
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

# Configuration
BASE_URL = "http://localhost:8881"
TIMEOUT = 30

class EndpointDiscoveryAnalyzer:
    """Analyzes all endpoints and provides cleanup recommendations"""
    
    def __init__(self):
        self.discovered_endpoints = set()
        self.endpoint_results = {}
        self.functionality_map = {}
        
        # Define all known endpoints from codebase analysis
        self.known_endpoints = {
            # Core Analysis Endpoints
            'core_analysis': [
                ('POST', '/analyze', 'Three-model ensemble analysis'),
                ('POST', '/extract_phrases', 'Crisis phrase extraction'),
                ('POST', '/analyze_message', 'Alternative analysis endpoint (potential)'),
                ('POST', '/batch_analysis', 'Batch analysis endpoint (potential)')
            ],
            
            # Health & Status Endpoints
            'health_status': [
                ('GET', '/health', 'System health check'),
                ('GET', '/stats', 'Service statistics'),
                ('GET', '/status', 'Basic status (potential duplicate)')
            ],
            
            # Admin Label Management Endpoints
            'admin_labels': [
                ('GET', '/admin/status', 'Admin system status'),
                ('GET', '/admin/labels/status', 'Label configuration status'),
                ('POST', '/admin/labels/simple-switch', 'Simple label switching'),
                ('GET', '/admin/labels/config', 'Comprehensive configuration info'),
                ('GET', '/admin/labels/current', 'Current label set information'),
                ('GET', '/admin/labels/list', 'List all available label sets'),
                ('POST', '/admin/labels/switch', 'Full label set switching'),
                ('GET', '/admin/labels/details/{name}', 'Detailed label set info'),
                ('POST', '/admin/labels/reload', 'Reload from JSON configuration'),
                ('GET', '/admin/labels/validate', 'Validate current configuration'),
                ('GET', '/admin/labels/export/{name}', 'Export specific label set'),
                ('POST', '/admin/labels/test/mapping', 'Test label mapping'),
                ('POST', '/admin/labels/test/comprehensive', 'Trigger comprehensive test')
            ],
            
            # Ensemble Configuration Endpoints
            'ensemble_config': [
                ('GET', '/ensemble/config', 'Ensemble configuration'),
                ('GET', '/ensemble/health', 'Ensemble health'),
                ('GET', '/ensemble/status', 'Ensemble status')
            ],
            
            # Learning System Endpoints
            'learning_system': [
                ('GET', '/learning_statistics', 'Learning system metrics'),
                ('POST', '/analyze_false_negative', 'Analyze missed crises'),
                ('POST', '/analyze_false_positive', 'Analyze over-detections'),
                ('POST', '/update_learning_model', 'Update model with corrections')
            ],
            
            # Potential Admin System Endpoints
            'admin_system': [
                ('GET', '/admin/models/status', 'Admin model status (potential)'),
                ('GET', '/admin/system/status', 'Admin system status (potential)'),
                ('POST', '/admin/system/restart', 'System restart (potential)'),
                ('GET', '/admin/logs', 'System logs (potential)')
            ],
            
            # Documentation & Metadata
            'documentation': [
                ('GET', '/docs', 'API documentation'),
                ('GET', '/openapi.json', 'OpenAPI specification'),
                ('GET', '/redoc', 'ReDoc documentation'),
                ('GET', '/version', 'Version information'),
                ('GET', '/metrics', 'Prometheus metrics (potential)')
            ]
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
            except Exception:
                pass
            
            if attempt < max_attempts - 1:
                time.sleep(delay)
        
        return False

    def test_endpoint(self, method: str, endpoint: str, description: str) -> Dict[str, Any]:
        """Test a single endpoint and return detailed results"""
        
        # Handle parameterized endpoints with test values
        test_endpoint = endpoint
        if '{name}' in endpoint:
            test_endpoint = endpoint.replace('{name}', 'crisis_mental_health')
        
        result = {
            'method': method,
            'endpoint': endpoint,
            'test_endpoint': test_endpoint,
            'description': description,
            'status_code': None,
            'success': False,
            'response_data': None,
            'error': None,
            'notes': [],
            'cleanup_recommendation': 'keep',
            'tested_at': datetime.now().isoformat()
        }
        
        try:
            if method == 'GET':
                response = requests.get(f"{BASE_URL}{test_endpoint}", timeout=TIMEOUT)
            elif method == 'POST':
                # Provide appropriate payload based on endpoint
                payload = self._get_test_payload(test_endpoint)
                response = requests.post(f"{BASE_URL}{test_endpoint}", json=payload, timeout=TIMEOUT)
            else:
                result['error'] = f"Unsupported method: {method}"
                return result
            
            result['status_code'] = response.status_code
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    result['response_data'] = data
                    result['success'] = True
                    result['notes'].append("Returns valid JSON")
                    
                    # Additional validation based on endpoint type
                    self._validate_response_schema(test_endpoint, data, result)
                    
                except json.JSONDecodeError:
                    result['notes'].append("Non-JSON response")
                    result['cleanup_recommendation'] = 'investigate'
                    
            elif response.status_code == 404:
                result['error'] = "Not found"
                result['cleanup_recommendation'] = 'remove'
                result['notes'].append("Dead endpoint - recommend removal")
                
            elif response.status_code in [400, 422]:
                result['error'] = f"Client error: {response.status_code}"
                result['notes'].append("May need different payload or parameters")
                result['cleanup_recommendation'] = 'investigate'
                
            elif response.status_code == 500:
                result['error'] = "Internal server error"
                result['cleanup_recommendation'] = 'fix'
                result['notes'].append("Server-side issue needs fixing")
                
            else:
                result['error'] = f"Unexpected status: {response.status_code}"
                result['cleanup_recommendation'] = 'investigate'
            
        except requests.exceptions.Timeout:
            result['error'] = "Request timeout"
            result['cleanup_recommendation'] = 'investigate'
            result['notes'].append("May be slow or hanging")
            
        except Exception as e:
            result['error'] = str(e)
            result['cleanup_recommendation'] = 'investigate'
            result['notes'].append(f"Exception: {type(e).__name__}")
        
        return result

    def _get_test_payload(self, endpoint: str) -> Dict[str, Any]:
        """Get appropriate test payload for POST endpoints"""
        
        # Analysis endpoints
        if '/analyze' in endpoint and endpoint != '/analyze_false_negative' and endpoint != '/analyze_false_positive':
            return {
                'message': 'Test message for analysis',
                'user_id': 'test_user',
                'channel_id': 'test_channel'
            }
        
        # Extract phrases
        elif '/extract_phrases' in endpoint:
            return {
                'message': 'Test message for phrase extraction',
                'user_id': 'test_user',
                'channel_id': 'test_channel',
                'parameters': {'min_phrase_length': 2, 'max_phrase_length': 6}
            }
        
        # Label switching
        elif '/labels/switch' in endpoint or '/simple-switch' in endpoint:
            return {'label_set': 'crisis_mental_health'}
        
        # Label mapping test
        elif '/test/mapping' in endpoint:
            return {'test_messages': ['test message'], 'validate_schema': True}
        
        # False negative analysis
        elif '/analyze_false_negative' in endpoint:
            return {
                'message': 'I dont want to be here',
                'should_detect_level': 'high',
                'actually_detected': 'low',
                'context': {'channel': 'support'},
                'severity_score': 8
            }
        
        # False positive analysis
        elif '/analyze_false_positive' in endpoint:
            return {
                'message': 'This game is killing me!',
                'detected_level': 'high',
                'correct_level': 'none',
                'context': {'channel': 'gaming'},
                'severity_score': 1
            }
        
        # Learning model update
        elif '/update_learning_model' in endpoint:
            return {
                'learning_record_id': 'test_001',
                'record_type': 'false_negative',
                'message_data': {'content': 'test message', 'user_id': 'test', 'channel_id': 'test'},
                'correction_data': {'should_detect_level': 'high', 'actually_detected': 'low'},
                'context_data': {'channel': 'support'}
            }
        
        # Default empty payload
        else:
            return {}

    def _validate_response_schema(self, endpoint: str, data: Dict[str, Any], result: Dict[str, Any]):
        """Validate response schema for known endpoints"""
        
        # Health endpoint validation
        if endpoint == '/health':
            required_fields = ['status', 'uptime', 'model_loaded']
            missing = [f for f in required_fields if f not in data]
            if missing:
                result['notes'].append(f"Missing required fields: {missing}")
            else:
                result['notes'].append("Health schema valid")
        
        # Analysis endpoint validation
        elif endpoint == '/analyze':
            required_fields = ['crisis_level', 'confidence_score', 'needs_response']
            missing = [f for f in required_fields if f not in data]
            if missing:
                result['notes'].append(f"Missing required fields: {missing}")
            else:
                crisis_level = data.get('crisis_level')
                confidence = data.get('confidence_score', 0)
                valid_levels = ['none', 'low', 'medium', 'high']
                
                if crisis_level in valid_levels and 0 <= confidence <= 1:
                    result['notes'].append("Analysis schema valid")
                else:
                    result['notes'].append("Analysis schema issues detected")
        
        # Admin label endpoints
        elif '/admin/labels/' in endpoint:
            if 'list' in endpoint:
                if 'sets' in data or 'available_sets' in data:
                    result['notes'].append("Label list schema valid")
                else:
                    result['notes'].append("Label list schema unexpected")
            elif 'status' in endpoint:
                if 'status' in data or 'current_label_set' in data:
                    result['notes'].append("Label status schema valid")
                else:
                    result['notes'].append("Label status schema unexpected")

    def run_discovery_analysis(self) -> Dict[str, Any]:
        """Run complete endpoint discovery and analysis"""
        logger.info("🚀 STARTING ENDPOINT DISCOVERY AND CLEANUP ANALYSIS")
        logger.info("🎯 Goal: Test all endpoints, identify dead code, provide cleanup recommendations")
        logger.info("=" * 100)
        
        # Wait for service
        if not self.wait_for_service_ready():
            logger.error("❌ Service not available - cannot run discovery")
            return {'success': False, 'error': 'Service not available'}
        
        discovery_results = {
            'functional_endpoints': [],
            'dead_endpoints': [],
            'broken_endpoints': [],
            'needs_investigation': [],
            'cleanup_recommendations': {},
            'category_analysis': {},
            'total_tested': 0,
            'total_functional': 0
        }
        
        # Test all known endpoints by category
        for category, endpoints in self.known_endpoints.items():
            logger.info(f"\n📁 TESTING CATEGORY: {category.upper()}")
            logger.info("=" * 60)
            
            category_results = {
                'total': len(endpoints),
                'functional': 0,
                'dead': 0,
                'broken': 0,
                'needs_investigation': 0,
                'endpoints': {}
            }
            
            for method, endpoint, description in endpoints:
                logger.info(f"🧪 Testing {method} {endpoint}...")
                
                result = self.test_endpoint(method, endpoint, description)
                self.endpoint_results[endpoint] = result
                category_results['endpoints'][endpoint] = result
                discovery_results['total_tested'] += 1
                
                # Categorize result
                if result['success']:
                    category_results['functional'] += 1
                    discovery_results['functional_endpoints'].append(endpoint)
                    discovery_results['total_functional'] += 1
                    logger.info(f"   ✅ {description}: Functional")
                    
                elif result['status_code'] == 404:
                    category_results['dead'] += 1
                    discovery_results['dead_endpoints'].append(endpoint)
                    logger.info(f"   💀 {description}: Dead (404)")
                    
                elif result['status_code'] in [500, 503]:
                    category_results['broken'] += 1
                    discovery_results['broken_endpoints'].append(endpoint)
                    logger.error(f"   🔧 {description}: Broken ({result['status_code']})")
                    
                else:
                    category_results['needs_investigation'] += 1
                    discovery_results['needs_investigation'].append(endpoint)
                    logger.warning(f"   🔍 {description}: Needs investigation ({result.get('status_code', 'Unknown')})")
                
                # Add notes if available
                if result.get('notes'):
                    logger.info(f"      📝 Notes: {', '.join(result['notes'])}")
                
                time.sleep(0.5)  # Brief pause between tests
            
            discovery_results['category_analysis'][category] = category_results
            
            # Category summary
            logger.info(f"\n📊 {category.upper()} SUMMARY:")
            logger.info(f"   ✅ Functional: {category_results['functional']}/{category_results['total']}")
            logger.info(f"   💀 Dead: {category_results['dead']}")
            logger.info(f"   🔧 Broken: {category_results['broken']}")
            logger.info(f"   🔍 Needs investigation: {category_results['needs_investigation']}")
        
        # Generate cleanup recommendations
        discovery_results['cleanup_recommendations'] = self._generate_cleanup_recommendations(discovery_results)
        
        # Print comprehensive analysis
        self._print_discovery_analysis(discovery_results)
        
        return discovery_results

    def _generate_cleanup_recommendations(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Generate specific cleanup recommendations"""
        
        recommendations = {
            'immediate_removal': [],
            'fix_required': [],
            'investigate_further': [],
            'keep_functional': [],
            'priority_actions': []
        }
        
        # Categorize endpoints by cleanup action needed
        for endpoint, result in self.endpoint_results.items():
            cleanup_rec = result.get('cleanup_recommendation', 'keep')
            
            if cleanup_rec == 'remove' or result.get('status_code') == 404:
                recommendations['immediate_removal'].append({
                    'endpoint': endpoint,
                    'reason': result.get('error', 'Not found'),
                    'description': result.get('description', '')
                })
                
            elif cleanup_rec == 'fix' or result.get('status_code') in [500, 503]:
                recommendations['fix_required'].append({
                    'endpoint': endpoint,
                    'error': result.get('error', 'Unknown error'),
                    'status_code': result.get('status_code'),
                    'description': result.get('description', '')
                })
                
            elif cleanup_rec == 'investigate':
                recommendations['investigate_further'].append({
                    'endpoint': endpoint,
                    'issue': result.get('error', 'Unknown issue'),
                    'status_code': result.get('status_code'),
                    'notes': result.get('notes', []),
                    'description': result.get('description', '')
                })
                
            elif result.get('success', False):
                recommendations['keep_functional'].append({
                    'endpoint': endpoint,
                    'description': result.get('description', ''),
                    'notes': result.get('notes', [])
                })
        
        # Generate priority actions
        if recommendations['fix_required']:
            recommendations['priority_actions'].append("🔧 Fix broken endpoints immediately")
        
        if len(recommendations['immediate_removal']) > 5:
            recommendations['priority_actions'].append("🗑️ Significant code cleanup needed - many dead endpoints")
        
        if results['total_functional'] < results['total_tested'] * 0.7:
            recommendations['priority_actions'].append("⚠️ System health concern - less than 70% endpoints functional")
        
        # Specific recommendations based on analysis
        core_analysis_dead = sum(1 for ep in recommendations['immediate_removal'] 
                               if any(core_ep[1] == ep['endpoint'] for core_ep in self.known_endpoints['core_analysis']))
        
        if core_analysis_dead > 0:
            recommendations['priority_actions'].append("🚨 CRITICAL: Core analysis endpoints are dead")
        
        admin_functional = sum(1 for ep in recommendations['keep_functional']
                             if '/admin/' in ep['endpoint'])
        
        if admin_functional < 3:
            recommendations['priority_actions'].append("⚠️ Admin functionality may be compromised")
        
        return recommendations

    def _print_discovery_analysis(self, results: Dict[str, Any]):
        """Print comprehensive discovery analysis"""
        logger.info(f"\n🔍 ENDPOINT DISCOVERY ANALYSIS")
        logger.info("=" * 100)
        
        # Overall statistics
        total_tested = results['total_tested']
        total_functional = results['total_functional']
        success_rate = (total_functional / total_tested * 100) if total_tested > 0 else 0
        
        logger.info(f"📊 OVERALL STATISTICS:")
        logger.info(f"   🧪 Total endpoints tested: {total_tested}")
        logger.info(f"   ✅ Functional endpoints: {total_functional}")
        logger.info(f"   💀 Dead endpoints: {len(results['dead_endpoints'])}")
        logger.info(f"   🔧 Broken endpoints: {len(results['broken_endpoints'])}")
        logger.info(f"   🔍 Need investigation: {len(results['needs_investigation'])}")
        logger.info(f"   📈 Success rate: {success_rate:.1f}%")
        
        # Category breakdown
        logger.info(f"\n📁 CATEGORY BREAKDOWN:")
        for category, analysis in results['category_analysis'].items():
            logger.info(f"   {category}: {analysis['functional']}/{analysis['total']} functional")
        
        # Cleanup recommendations
        recommendations = results['cleanup_recommendations']
        
        if recommendations['immediate_removal']:
            logger.info(f"\n💀 IMMEDIATE REMOVAL CANDIDATES ({len(recommendations['immediate_removal'])}):")
            for item in recommendations['immediate_removal']:
                logger.info(f"   ❌ {item['endpoint']} - {item['reason']}")
        
        if recommendations['fix_required']:
            logger.info(f"\n🔧 ENDPOINTS NEEDING FIXES ({len(recommendations['fix_required'])}):")
            for item in recommendations['fix_required']:
                logger.info(f"   🔧 {item['endpoint']} - {item['error']} (Status: {item['status_code']})")
        
        if recommendations['investigate_further']:
            logger.info(f"\n🔍 ENDPOINTS NEEDING INVESTIGATION ({len(recommendations['investigate_further'])}):")
            for item in recommendations['investigate_further']:
                logger.info(f"   🔍 {item['endpoint']} - {item['issue']} (Status: {item['status_code']})")
        
        if recommendations['priority_actions']:
            logger.info(f"\n🎯 PRIORITY ACTIONS:")
            for action in recommendations['priority_actions']:
                logger.info(f"   {action}")
        
        # Code cleanup recommendations
        logger.info(f"\n📝 CODE CLEANUP RECOMMENDATIONS:")
        
        removal_count = len(recommendations['immediate_removal'])
        if removal_count > 0:
            logger.info(f"   🗑️ Remove {removal_count} dead endpoints to clean up codebase")
            
        fix_count = len(recommendations['fix_required'])
        if fix_count > 0:
            logger.info(f"   🔧 Fix {fix_count} broken endpoints to restore functionality")
        
        functional_count = len(recommendations['keep_functional'])
        logger.info(f"   ✅ Keep {functional_count} functional endpoints")
        
        # System health assessment
        logger.info(f"\n🏥 SYSTEM HEALTH ASSESSMENT:")
        if success_rate >= 90:
            logger.info(f"   🎉 EXCELLENT: System is in great shape ({success_rate:.1f}%)")
        elif success_rate >= 75:
            logger.info(f"   ✅ GOOD: System is mostly functional ({success_rate:.1f}%)")
        elif success_rate >= 50:
            logger.info(f"   ⚠️ NEEDS ATTENTION: Moderate issues detected ({success_rate:.1f}%)")
        else:
            logger.error(f"   ❌ CRITICAL: Major system issues ({success_rate:.1f}%)")

    def generate_cleanup_script_recommendations(self, results: Dict[str, Any]):
        """Generate specific code cleanup recommendations"""
        logger.info(f"\n📜 CLEANUP SCRIPT RECOMMENDATIONS")
        logger.info("=" * 60)
        
        removal_candidates = results['cleanup_recommendations']['immediate_removal']
        
        if removal_candidates:
            logger.info(f"🗑️ RECOMMENDED CODE REMOVALS:")
            
            # Group by file
            file_removals = {}
            for item in removal_candidates:
                endpoint = item['endpoint']
                
                # Determine likely file location
                if '/admin/' in endpoint:
                    file_location = 'api/admin_endpoints.py'
                elif '/ensemble/' in endpoint:
                    file_location = 'api/ensemble_endpoints.py'
                elif '/learning' in endpoint or 'false_' in endpoint:
                    file_location = 'api/learning_endpoints.py'
                elif endpoint in ['/stats', '/status', '/health']:
                    file_location = 'main.py'
                else:
                    file_location = 'main.py or unknown'
                
                if file_location not in file_removals:
                    file_removals[file_location] = []
                file_removals[file_location].append(item)
            
            for file_path, endpoints in file_removals.items():
                logger.info(f"\n   📁 {file_path}:")
                for item in endpoints:
                    logger.info(f"      ❌ Remove: {item['endpoint']} ({item['reason']})")
        
        # Generate specific action items
        logger.info(f"\n🎯 IMMEDIATE ACTION ITEMS:")
        
        action_count = 1
        
        if removal_candidates:
            logger.info(f"   {action_count}. Remove {len(removal_candidates)} dead endpoints from codebase")
            action_count += 1
        
        fix_candidates = results['cleanup_recommendations']['fix_required']
        if fix_candidates:
            logger.info(f"   {action_count}. Fix {len(fix_candidates)} broken endpoints")
            action_count += 1
        
        investigate_candidates = results['cleanup_recommendations']['investigate_further']
        if investigate_candidates:
            logger.info(f"   {action_count}. Investigate {len(investigate_candidates)} problematic endpoints")
            action_count += 1
        
        functional_count = len(results['cleanup_recommendations']['keep_functional'])
        logger.info(f"   {action_count}. Document {functional_count} functional endpoints")

def main():
    """Main execution"""
    analyzer = EndpointDiscoveryAnalyzer()
    results = analyzer.run_discovery_analysis()
    
    if results.get('success', True):  # Default to True unless explicitly failed
        analyzer.generate_cleanup_script_recommendations(results)
        
        logger.info(f"\n🏁 ENDPOINT DISCOVERY COMPLETE")
        
        # Determine overall success
        total_tested = results['total_tested']
        total_functional = results['total_functional']
        success_rate = (total_functional / total_tested * 100) if total_tested > 0 else 0
        
        # Success criteria: At least 70% functional AND core endpoints working
        core_analysis_functional = any('/analyze' in ep for ep in results['functional_endpoints'])
        admin_functional = any('/admin/' in ep for ep in results['functional_endpoints'])
        health_functional = any('/health' in ep for ep in results['functional_endpoints'])
        
        essential_functional = core_analysis_functional and admin_functional and health_functional
        
        overall_success = success_rate >= 70 and essential_functional
        
        if overall_success:
            logger.info(f"🎉 DISCOVERY SUCCESS: System endpoints are in good shape")
            logger.info(f"✅ Core functionality preserved after Phase 3a migration")
        else:
            logger.error(f"❌ DISCOVERY ISSUES: System needs attention")
            logger.error(f"🔧 Essential endpoints or success rate below threshold")
        
        return overall_success
    else:
        logger.error(f"❌ DISCOVERY FAILED: {results.get('error')}")
        return False

if __name__ == "__main__":
    import sys
    success = main()
    sys.exit(0 if success else 1)