#!/usr/bin/env python3
"""
API-Based Performance Test - Tests the actual running server
Tests performance against the /analyze endpoint via HTTP requests

FILE: tests/test_api_performance.py
VERSION: v3.1-3e-7-api
"""

import sys
import os
import time
import requests
import statistics
import json
from typing import Dict, Any, List

# Import colorlog for colored output
try:
    import colorlog
except ImportError:
    print("❌ colorlog not installed. Install with: pip install colorlog")
    sys.exit(1)

def setup_logger():
    """Setup colored logging"""
    formatter = colorlog.ColoredFormatter(
        '%(log_color)s%(message)s%(reset)s',
        reset=True,
        log_colors={
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'red,bg_white',
        }
    )
    
    import logging
    console_handler = colorlog.StreamHandler()
    console_handler.setFormatter(formatter)
    
    logger = logging.getLogger('APIPerformanceTest')
    logger.setLevel(logging.INFO)
    logger.handlers = [console_handler]
    
    return logger

def get_server_config():
    """Get server configuration"""
    # Default configuration - adjust if different
    return {
        'host': 'localhost',
        'port': 8881,
        'base_url': 'http://localhost:8881'
    }

def test_server_health(server_config):
    """Test if server is running and responsive"""
    try:
        health_url = f"{server_config['base_url']}/health"
        response = requests.get(health_url, timeout=10)
        
        if response.status_code == 200:
            health_data = response.json()
            return True, health_data
        else:
            return False, f"Health check returned {response.status_code}"
            
    except requests.exceptions.ConnectionError:
        return False, "Connection refused - server may not be running"
    except requests.exceptions.Timeout:
        return False, "Health check timed out"
    except Exception as e:
        return False, f"Health check failed: {e}"

def get_server_status(server_config):
    """Get comprehensive server status including warmup info"""
    try:
        # Try /health endpoint for detailed status
        health_url = f"{server_config['base_url']}/health"
        response = requests.get(health_url, timeout=10)
        
        if response.status_code == 200:
            return True, response.json()
        else:
            return False, f"Health endpoint returned {response.status_code}"
            
    except Exception as e:
        return False, f"Health endpoint failed: {e}"

def test_api_crisis_analysis_performance(logger, server_config):
    """Test crisis analysis performance via API calls"""
    logger.info("🚨 Testing API crisis analysis performance...")
    
    analyze_url = f"{server_config['base_url']}/analyze"
    target_time = 500  # ms
    
    test_messages = [
        "I'm having a really difficult time and feeling overwhelmed with everything.",
        "This is getting harder every day and I don't see a way out.",
        "I feel like I'm drowning in all these problems and can't cope.",
        "Everything seems hopeless right now and I need help.",
        "I'm struggling to manage and feeling completely lost."
    ]
    
    print(f"\n⚡ Running {len(test_messages)} API performance tests...")
    analysis_times = []
    results = []
    
    for i, test_message in enumerate(test_messages):
        try:
            # Prepare request payload
            payload = {
                "message": test_message,
                "user_id": f"api_perf_user_{i}",
                "channel_id": "api_perf_test_channel"
            }
            
            # Make API request with timing
            start_time = time.time()
            response = requests.post(
                analyze_url, 
                json=payload,
                timeout=30,  # 30 second timeout
                headers={'Content-Type': 'application/json'}
            )
            request_time = (time.time() - start_time) * 1000
            
            if response.status_code == 200:
                result_data = response.json()
                analysis_times.append(request_time)
                results.append(result_data)
                
                status_indicator = "🟢" if request_time <= target_time else "🟡" if request_time <= target_time * 1.2 else "🔴"
                print(f"   {status_indicator} API Call {i+1}: {request_time:.1f}ms")
            else:
                print(f"   ❌ API Call {i+1} failed: HTTP {response.status_code}")
                try:
                    error_data = response.json()
                    print(f"      Error: {error_data.get('error', 'Unknown error')}")
                except:
                    print(f"      Error: {response.text}")
                
        except requests.exceptions.Timeout:
            print(f"   ⏰ API Call {i+1} timed out (>30s)")
        except requests.exceptions.ConnectionError:
            print(f"   ❌ API Call {i+1} connection failed")
        except Exception as e:
            print(f"   ❌ API Call {i+1} failed: {e}")
    
    if analysis_times and results:
        avg_time = statistics.mean(analysis_times)
        min_time = min(analysis_times)
        max_time = max(analysis_times)
        median_time = statistics.median(analysis_times)
        
        print("\n" + "=" * 80)
        print("📊 API CRISIS ANALYSIS PERFORMANCE")
        print("=" * 80)
        print(f"TARGET: {target_time}ms per API call")
        print(f"AVERAGE: {avg_time:.1f}ms")
        print(f"MEDIAN: {median_time:.1f}ms")
        print(f"FASTEST: {min_time:.1f}ms")
        print(f"SLOWEST: {max_time:.1f}ms")
        print(f"CONSISTENCY: {max_time - min_time:.1f}ms variance")
        print(f"SUCCESS RATE: {len(analysis_times)}/{len(test_messages)} ({len(analysis_times)/len(test_messages)*100:.1f}%)")
        
        # Performance evaluation
        if avg_time <= target_time:
            print("🚀 API PERFORMANCE: TARGET ACHIEVED!")
            performance_status = "TARGET_ACHIEVED"
        elif avg_time <= target_time * 1.1:
            print("✅ API PERFORMANCE: VERY CLOSE TO TARGET")
            performance_status = "VERY_CLOSE"
        elif avg_time <= target_time * 1.2:
            print("⚠️ API PERFORMANCE: NEEDS MINOR OPTIMIZATION")
            performance_status = "MINOR_OPT_NEEDED"
        else:
            gap = avg_time - target_time
            improvement_pct = ((avg_time / target_time) - 1) * 100
            print(f"❌ API PERFORMANCE GAP: {gap:.1f}ms over target")
            print(f"IMPROVEMENT NEEDED: {improvement_pct:.1f}% speed increase")
            performance_status = "MAJOR_OPT_NEEDED"
        
        # Analyze first result for crisis detection functionality
        if results:
            first_result = results[0]
            print(f"\n🔍 API RESPONSE ANALYSIS (First Result):")
            print(f"   Status: {first_result.get('status', 'Unknown')}")
            print(f"   Crisis Level: {first_result.get('crisis_level', 'Unknown')}")
            print(f"   Confidence: {first_result.get('confidence', 'Unknown')}")
            print(f"   Analysis Time: {first_result.get('analysis_time_ms', 'Unknown')}ms")
            print(f"   Models Used: {first_result.get('models_used', 'Unknown')}")
            
            # Check for warmup indicators
            if 'model_coordination_manager' in first_result:
                mcm_info = first_result['model_coordination_manager']
                if 'warmup_status' in mcm_info:
                    warmup_info = mcm_info['warmup_status']
                    print(f"   Pipeline Warmed: {warmup_info.get('pipeline_warmed', 'Unknown')}")
                    print(f"   Cold Start Eliminated: {warmup_info.get('cold_start_eliminated', 'Unknown')}")
        
        # Warmup effectiveness (compare first vs later runs)
        if len(analysis_times) > 1:
            first_run = analysis_times[0]
            later_runs_avg = statistics.mean(analysis_times[1:])
            variance = abs(first_run - later_runs_avg)
            
            print(f"\n🔥 WARMUP EFFECTIVENESS (API Level):")
            print(f"   First API Call: {first_run:.1f}ms")
            print(f"   Later Calls Average: {later_runs_avg:.1f}ms")
            print(f"   First-to-Later Variance: {variance:.1f}ms")
            
            if variance <= 50:  # Less than 50ms variance indicates good warmup
                print("🚀 WARMUP HIGHLY EFFECTIVE (consistent performance)")
                warmup_effectiveness = "HIGHLY_EFFECTIVE"
            elif variance <= 100:
                print("✅ WARMUP MODERATELY EFFECTIVE")
                warmup_effectiveness = "MODERATELY_EFFECTIVE"
            else:
                print("⚠️ WARMUP MAY NEED IMPROVEMENT (high variance)")
                warmup_effectiveness = "NEEDS_IMPROVEMENT"
        else:
            warmup_effectiveness = "INSUFFICIENT_DATA"
        
        print("=" * 80)
        
        return {
            'avg_time_ms': avg_time,
            'median_time_ms': median_time,
            'min_time_ms': min_time,
            'max_time_ms': max_time,
            'target_ms': target_time,
            'performance_status': performance_status,
            'target_achieved': avg_time <= target_time,
            'first_run_time_ms': analysis_times[0] if analysis_times else 0,
            'consistency_ms': max_time - min_time,
            'success_rate': len(analysis_times) / len(test_messages),
            'warmup_effectiveness': warmup_effectiveness,
            'total_requests': len(test_messages),
            'successful_requests': len(analysis_times)
        }
    else:
        print("❌ No successful API calls - cannot assess performance")
        return None

def main():
    """Main API performance testing function"""
    logger = setup_logger()
    
    print("🌈" * 30)
    print("🚀 API PERFORMANCE TEST - LIVE SERVER")
    print("🏳️‍🌈 The Alphabet Cartel - Crisis Detection System")
    print("🌈" * 30)
    
    server_config = get_server_config()
    total_start = time.time()
    
    # Test 1: Server Health Check
    print(f"\n🏥 TEST 1: Server Health Check")
    print("-" * 50)
    print(f"Testing server at: {server_config['base_url']}")
    
    health_ok, health_data = test_server_health(server_config)
    if not health_ok:
        print(f"❌ Server health check failed: {health_data}")
        print("\nMake sure the server is running with:")
        print("  docker compose up ash-nlp")
        return {}
    
    print("✅ Server is healthy and responsive")
    if isinstance(health_data, dict):
        print(f"   Server Status: {health_data.get('status', 'Unknown')}")
        print(f"   Version: {health_data.get('version', 'Unknown')}")
    
    # Test 2: Server Status (including warmup info)
    print(f"\n📊 TEST 2: Server Health & Warmup Info")
    print("-" * 50)
    
    status_ok, status_data = get_server_status(server_config)
    if status_ok and isinstance(status_data, dict):
        print("✅ Detailed server health retrieved successfully")
        
        # Look for warmup information in health response
        if 'model_coordination_manager' in status_data:
            mcm_status = status_data['model_coordination_manager']
            print(f"   Models Loaded: {mcm_status.get('models_configured', 'Unknown')}")
            
            if 'warmup_status' in mcm_status:
                warmup_status = mcm_status['warmup_status']
                print(f"   Pipeline Warmed: {warmup_status.get('pipeline_warmed', 'Unknown')}")
                print(f"   Warmup Success: {warmup_status.get('warmup_success', 'Unknown')}")
                print(f"   Cold Start Eliminated: {warmup_status.get('cold_start_eliminated', 'Unknown')}")
                print(f"   Ready for Production: {warmup_status.get('ready_for_production', 'Unknown')}")
            else:
                print("   ⚠️ No warmup status found in health response")
        else:
            print("   ⚠️ No model coordination manager status found in health response")
    else:
        print(f"⚠️ Could not retrieve detailed status from /health: {status_data}")
    
    # Test 3: API Performance
    print(f"\n🚨 TEST 3: API Crisis Analysis Performance")
    print("-" * 50)
    
    api_results = test_api_crisis_analysis_performance(logger, server_config)
    
    total_test_time = time.time() - total_start
    
    # Final Summary
    print("\n" + "🌈" * 30)
    print("📊 API PERFORMANCE SUMMARY")
    print("🌈" * 30)
    
    print(f"\nTotal Test Duration: {total_test_time:.1f}s")
    print(f"Server: {server_config['base_url']}")
    
    if api_results:
        print(f"\n🚨 API CRISIS ANALYSIS:")
        print(f"   Target: {api_results.get('target_ms', 0)}ms per request")
        print(f"   Average: {api_results.get('avg_time_ms', 0):.1f}ms")
        print(f"   First Request: {api_results.get('first_run_time_ms', 0):.1f}ms")
        print(f"   Performance Status: {api_results.get('performance_status', 'Unknown')}")
        print(f"   Target Achieved: {api_results.get('target_achieved', False)}")
        print(f"   Success Rate: {api_results.get('success_rate', 0)*100:.1f}%")
        print(f"   Warmup Effectiveness: {api_results.get('warmup_effectiveness', 'Unknown')}")
        print(f"   Consistency: {api_results.get('consistency_ms', 0):.1f}ms variance")
        
        # Overall assessment
        target_achieved = api_results.get('target_achieved', False)
        success_rate_good = api_results.get('success_rate', 0) >= 0.8
        warmup_effective = api_results.get('warmup_effectiveness') in ['HIGHLY_EFFECTIVE', 'MODERATELY_EFFECTIVE']
        
        print(f"\n🎯 OVERALL API ASSESSMENT:")
        if target_achieved and success_rate_good and warmup_effective:
            print("   🚀 EXCELLENT - All API performance targets achieved!")
        elif target_achieved and success_rate_good:
            print("   ✅ GOOD - API performance targets achieved")
        elif success_rate_good:
            print("   ⚠️ PARTIAL - API functional but needs performance optimization")
        else:
            print("   ❌ NEEDS WORK - API performance and/or reliability issues")
    else:
        print("\n❌ API performance testing failed - check server status")
    
    print(f"\n🏳️‍🌈 API performance testing complete!")
    return {'api_results': api_results, 'server_config': server_config}

if __name__ == '__main__':
    main()