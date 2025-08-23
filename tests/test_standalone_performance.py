#!/usr/bin/env python3
"""
Standalone Performance Test - Direct Output Without unittest Buffering
Shows all performance metrics in real-time with warmup validation

FILE: tests/standalone_performance_test.py
VERSION: v3.1-3e-7-warmup
"""

import sys
import os
import time
import asyncio
import statistics
from typing import Dict, Any, List

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

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
    
    logger = logging.getLogger('PerformanceTest')
    logger.setLevel(logging.INFO)
    logger.handlers = [console_handler]
    
    return logger

def test_system_initialization_with_warmup(logger):
    """Test system initialization including warmup timing"""
    logger.info("🚀 Testing system initialization with warmup...")
    
    try:
        from main import initialize_unified_managers
        
        print("\n🔧 Initializing system with model preloading and pipeline warmup...")
        init_start = time.time()
        managers = initialize_unified_managers()
        total_init_time = (time.time() - init_start) * 1000
        
        print(f"✅ Complete system initialization: {total_init_time:.1f}ms")
        
        # Check warmup status
        model_manager = managers.get('model_coordination_manager')
        if not model_manager:
            print("❌ ModelCoordinationManager not available")
            return None, managers
        
        warmup_status = model_manager.get_warmup_status()
        
        print("\n" + "=" * 60)
        print("🔥 SYSTEM INITIALIZATION & WARMUP STATUS")
        print("=" * 60)
        print(f"Total Init Time: {total_init_time:.1f}ms")
        print(f"Pipeline Warmed: {warmup_status.get('pipeline_warmed', False)}")
        print(f"Warmup Success: {warmup_status.get('warmup_success', 'Unknown')}")
        print(f"Models Preloaded: {warmup_status.get('models_preloaded', False)}")
        print(f"Models Cached: {warmup_status.get('models_cached', 0)}")
        print(f"Cold Start Eliminated: {warmup_status.get('cold_start_eliminated', False)}")
        print(f"Ready for Production: {warmup_status.get('ready_for_production', False)}")
        
        if warmup_status.get('total_warmup_time_ms'):
            warmup_time = warmup_status['total_warmup_time_ms']
            init_without_warmup = total_init_time - warmup_time
            print(f"Warmup Time: {warmup_time:.1f}ms")
            print(f"Init Without Warmup: {init_without_warmup:.1f}ms")
            print(f"Warmup Overhead: {(warmup_time/total_init_time)*100:.1f}% of total init")
        
        if warmup_status.get('warmup_analysis_time_ms'):
            print(f"Warmup Analysis Time: {warmup_status['warmup_analysis_time_ms']:.1f}ms")
        
        print("=" * 60)
        
        return {
            'total_init_time_ms': total_init_time,
            'warmup_status': warmup_status
        }, managers
        
    except Exception as e:
        print(f"❌ System initialization failed: {e}")
        import traceback
        traceback.print_exc()
        return None, None

def test_crisis_analysis_performance_post_warmup(logger, managers):
    """Test crisis analysis performance after warmup - focused and fast"""
    logger.info("🚨 Testing post-warmup crisis analysis performance...")
    
    try:
        crisis_analyzer = managers.get('crisis_analyzer')
        if not crisis_analyzer:
            print("❌ CrisisAnalyzer not available")
            return None
            
        # Performance test - reduced runs for faster testing
        target_time = 500  # ms
        test_messages = [
            "I'm having a really difficult time and feeling overwhelmed with everything.",
            "This is getting harder every day and I don't see a way out.",
            "I feel like I'm drowning in all these problems and can't cope.",
            "Everything seems hopeless right now and I need help.",
            "I'm struggling to manage and feeling completely lost."
        ]
        
        print(f"\n⚡ Running {len(test_messages)} post-warmup performance tests...")
        analysis_times = []
        
        for i, test_message in enumerate(test_messages):
            try:
                start_time = time.time()
                
                if hasattr(crisis_analyzer, 'analyze_message'):
                    import inspect
                    if asyncio.iscoroutinefunction(crisis_analyzer.analyze_message):
                        result = asyncio.run(crisis_analyzer.analyze_message(
                            test_message,
                            user_id=f"perf_user_{i}",
                            channel_id="perf_test_channel"
                        ))
                    else:
                        result = crisis_analyzer.analyze_message(
                            test_message,
                            user_id=f"perf_user_{i}",
                            channel_id="perf_test_channel"
                        )
                elif hasattr(crisis_analyzer, 'analyze'):
                    result = crisis_analyzer.analyze(test_message)
                else:
                    print("❌ No analysis method available")
                    return None
                    
                analysis_time = (time.time() - start_time) * 1000
                analysis_times.append(analysis_time)
                
                status_indicator = "🟢" if analysis_time <= target_time else "🟡" if analysis_time <= target_time * 1.2 else "🔴"
                print(f"   {status_indicator} Run {i+1}: {analysis_time:.1f}ms")
                
            except Exception as e:
                print(f"   ❌ Run {i+1} failed: {e}")
                
        if analysis_times:
            avg_time = statistics.mean(analysis_times)
            min_time = min(analysis_times)
            max_time = max(analysis_times)
            median_time = statistics.median(analysis_times)
            
            print("\n" + "=" * 80)
            print("📊 POST-WARMUP CRISIS ANALYSIS PERFORMANCE")
            print("=" * 80)
            print(f"TARGET: {target_time}ms per analysis")
            print(f"AVERAGE: {avg_time:.1f}ms")
            print(f"MEDIAN: {median_time:.1f}ms")
            print(f"FASTEST: {min_time:.1f}ms")
            print(f"SLOWEST: {max_time:.1f}ms")
            print(f"CONSISTENCY: {max_time - min_time:.1f}ms variance")
            
            # Performance evaluation
            if avg_time <= target_time:
                print("🚀 PERFORMANCE: TARGET ACHIEVED!")
                performance_status = "TARGET_ACHIEVED"
            elif avg_time <= target_time * 1.1:
                print("✅ PERFORMANCE: VERY CLOSE TO TARGET")
                performance_status = "VERY_CLOSE"
            elif avg_time <= target_time * 1.2:
                print("⚠️ PERFORMANCE: NEEDS MINOR OPTIMIZATION")
                performance_status = "MINOR_OPT_NEEDED"
            else:
                gap = avg_time - target_time
                improvement_pct = ((avg_time / target_time) - 1) * 100
                print(f"❌ PERFORMANCE GAP: {gap:.1f}ms over target")
                print(f"IMPROVEMENT NEEDED: {improvement_pct:.1f}% speed increase")
                performance_status = "MAJOR_OPT_NEEDED"
                
                print("\n🔧 OPTIMIZATION RECOMMENDATIONS:")
                if avg_time > 1000:
                    print("   - Implement aggressive result caching")
                    print("   - Consider model quantization")
                elif avg_time > 750:
                    print("   - Cache frequently accessed patterns")
                    print("   - Optimize model inference pipeline")
                else:
                    print("   - Fine-tune helper class operations")
                    print("   - Optimize configuration access patterns")
            
            # Warmup effectiveness analysis
            expected_cold_start = 1177  # ms from previous testing
            first_run_time = analysis_times[0] if analysis_times else 0
            penalty_avoided = expected_cold_start - first_run_time
            
            print(f"\n🔥 WARMUP EFFECTIVENESS ANALYSIS:")
            print(f"Expected Cold Start: {expected_cold_start}ms")
            print(f"Actual First Run: {first_run_time:.1f}ms")
            print(f"Cold Start Penalty Avoided: {penalty_avoided:.1f}ms")
            print(f"Performance Improvement: {(penalty_avoided/expected_cold_start)*100:.1f}%")
            
            if penalty_avoided >= 500:
                print("🚀 WARMUP HIGHLY EFFECTIVE")
                warmup_effectiveness = "HIGHLY_EFFECTIVE"
            elif penalty_avoided >= 300:
                print("✅ WARMUP MODERATELY EFFECTIVE")
                warmup_effectiveness = "MODERATELY_EFFECTIVE"
            elif penalty_avoided >= 100:
                print("⚠️ WARMUP PARTIALLY EFFECTIVE")
                warmup_effectiveness = "PARTIALLY_EFFECTIVE"
            else:
                print("❌ WARMUP NOT EFFECTIVE")
                warmup_effectiveness = "NOT_EFFECTIVE"
                
            print("=" * 80)
            
            return {
                'avg_time_ms': avg_time,
                'median_time_ms': median_time,
                'min_time_ms': min_time,
                'max_time_ms': max_time,
                'target_ms': target_time,
                'performance_status': performance_status,
                'target_achieved': avg_time <= target_time,
                'first_run_time_ms': first_run_time,
                'penalty_avoided_ms': penalty_avoided,
                'warmup_effectiveness': warmup_effectiveness,
                'consistency_ms': max_time - min_time
            }
            
    except Exception as e:
        print(f"❌ Performance test failed: {e}")
        import traceback
        traceback.print_exc()
        return None

def test_configuration_performance(logger, managers):
    """Test configuration access performance - quick check"""
    logger.info("⚙️ Testing configuration access performance...")
    
    try:
        unified_config = managers.get('unified_config')
        if not unified_config:
            print("❌ UnifiedConfig not available")
            return None
        
        target_time = 10  # ms per access
        
        # Reduced test set for faster execution
        test_configs = [
            ('GLOBAL_LOG_LEVEL', 'INFO'),
            ('NLP_SERVER_HOST', '0.0.0.0'),
            ('GLOBAL_NLP_API_PORT', 8881),
            ('NLP_ANALYSIS_ENABLE_ENSEMBLE', True)
        ]
        
        print("\n⚙️ Testing key configuration access speeds...")
        config_times = []
        
        for config_key, default_value in test_configs:
            try:
                start_time = time.time()
                
                if isinstance(default_value, bool):
                    value = unified_config.get_env_bool(config_key, default_value)
                elif isinstance(default_value, int):
                    value = unified_config.get_env_int(config_key, default_value)
                else:
                    value = unified_config.get_env(config_key, default_value)
                    
                access_time = (time.time() - start_time) * 1000
                config_times.append(access_time)
                
                status = "🟢" if access_time <= target_time else "🟡"
                print(f"   {status} {config_key}: {access_time:.3f}ms")
                
            except Exception as e:
                print(f"   ❌ {config_key} failed: {e}")
                
        if config_times:
            avg_time = statistics.mean(config_times)
            max_time = max(config_times)
            
            print("\n" + "=" * 50)
            print("📊 CONFIGURATION ACCESS PERFORMANCE")
            print("=" * 50)
            print(f"TARGET: <{target_time}ms per access")
            print(f"AVERAGE: {avg_time:.3f}ms")
            print(f"SLOWEST: {max_time:.3f}ms")
            
            if avg_time <= target_time:
                margin = target_time - avg_time
                print(f"✅ PERFORMANCE: {margin:.3f}ms under target")
                status = "EXCELLENT"
            else:
                excess = avg_time - target_time
                print(f"⚠️ PERFORMANCE: {excess:.3f}ms over target")
                status = "NEEDS_IMPROVEMENT"
                
            print("=" * 50)
            
            return {
                'avg_time_ms': avg_time,
                'max_time_ms': max_time,
                'target_ms': target_time,
                'status': status,
                'target_achieved': avg_time <= target_time
            }
            
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        return None

def main():
    """Main performance testing function - streamlined for speed"""
    logger = setup_logger()
    
    print("🌈" * 30)
    print("🚀 FAST PERFORMANCE TEST WITH WARMUP VALIDATION")
    print("🏳️‍🌈 The Alphabet Cartel - Crisis Detection System")
    print("🌈" * 30)
    
    total_start = time.time()
    results = {}
    
    # Test 1: System Initialization with Warmup
    print("\n🔧 TEST 1: System Initialization & Warmup")
    print("-" * 50)
    init_results, managers = test_system_initialization_with_warmup(logger)
    if init_results:
        results['initialization'] = init_results
    
    if not managers:
        print("❌ Cannot proceed without initialized managers")
        return results
    
    # Test 2: Configuration Performance (quick check)
    print("\n⚙️ TEST 2: Configuration Access Performance")
    print("-" * 50)
    config_results = test_configuration_performance(logger, managers)
    if config_results:
        results['configuration'] = config_results
    
    # Test 3: Post-Warmup Crisis Analysis Performance
    print("\n🚨 TEST 3: Post-Warmup Crisis Analysis Performance")
    print("-" * 50)
    crisis_results = test_crisis_analysis_performance_post_warmup(logger, managers)
    if crisis_results:
        results['crisis_analysis'] = crisis_results
    
    total_test_time = (time.time() - total_start)
    
    # Comprehensive Summary
    print("\n" + "🌈" * 30)
    print("📊 COMPREHENSIVE PERFORMANCE SUMMARY")
    print("🌈" * 30)
    
    print(f"\nTotal Test Duration: {total_test_time:.1f}s")
    
    # System Initialization Summary
    if 'initialization' in results:
        init = results['initialization']
        warmup = init.get('warmup_status', {})
        print(f"\n🔧 SYSTEM INITIALIZATION:")
        print(f"   Total Init Time: {init.get('total_init_time_ms', 0):.1f}ms")
        print(f"   Warmup Success: {warmup.get('warmup_success', 'Unknown')}")
        print(f"   Cold Start Eliminated: {warmup.get('cold_start_eliminated', False)}")
        print(f"   Production Ready: {warmup.get('ready_for_production', False)}")
    
    # Configuration Access Summary
    if 'configuration' in results:
        config = results['configuration']
        print(f"\n⚙️ CONFIGURATION ACCESS:")
        print(f"   Target: <{config.get('target_ms', 0)}ms")
        print(f"   Actual: {config.get('avg_time_ms', 0):.3f}ms")
        print(f"   Status: {config.get('status', 'Unknown')}")
    
    # Crisis Analysis Summary
    if 'crisis_analysis' in results:
        crisis = results['crisis_analysis']
        print(f"\n🚨 CRISIS ANALYSIS (POST-WARMUP):")
        print(f"   Target: {crisis.get('target_ms', 0)}ms")
        print(f"   Actual Average: {crisis.get('avg_time_ms', 0):.1f}ms")
        print(f"   First Run: {crisis.get('first_run_time_ms', 0):.1f}ms")
        print(f"   Performance: {crisis.get('performance_status', 'Unknown')}")
        print(f"   Target Achieved: {crisis.get('target_achieved', False)}")
        print(f"   Warmup Effectiveness: {crisis.get('warmup_effectiveness', 'Unknown')}")
        print(f"   Consistency: {crisis.get('consistency_ms', 0):.1f}ms variance")
        
        if crisis.get('penalty_avoided_ms', 0) > 0:
            print(f"   Cold Start Penalty Avoided: {crisis['penalty_avoided_ms']:.1f}ms")
    
    # Overall Assessment
    print(f"\n🎯 OVERALL ASSESSMENT:")
    
    config_good = results.get('configuration', {}).get('target_achieved', False)
    crisis_good = results.get('crisis_analysis', {}).get('target_achieved', False)
    warmup_effective = results.get('crisis_analysis', {}).get('warmup_effectiveness', '') in ['HIGHLY_EFFECTIVE', 'MODERATELY_EFFECTIVE']
    
    if crisis_good and config_good and warmup_effective:
        print("   🚀 EXCELLENT - All performance targets achieved with effective warmup!")
    elif crisis_good and warmup_effective:
        print("   ✅ GOOD - Crisis analysis targets achieved with effective warmup")
    elif warmup_effective:
        print("   ⚠️ PARTIAL - Warmup effective but performance needs optimization")
    else:
        print("   ❌ NEEDS WORK - Performance optimization and warmup tuning required")
    
    print(f"\n🏳️‍🌈 Fast performance testing complete in {total_test_time:.1f}s!")
    return results

if __name__ == '__main__':
    main()