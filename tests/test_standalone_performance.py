#!/usr/bin/env python3
"""
Standalone Performance Test - Direct Output Without unittest Buffering
Shows all performance metrics in real-time

FILE: tests/standalone_performance_test.py
VERSION: v3.1-3e-7-debug
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

def test_crisis_analysis_performance(logger):
    """Test crisis analysis performance with detailed metrics"""
    logger.info("🔧 Testing crisis analysis performance...")
    
    try:
        from main import initialize_unified_managers
        
        # Initialize system
        print("\n🚀 Initializing system...")
        start_time = time.time()
        managers = initialize_unified_managers()
        init_time = (time.time() - start_time) * 1000
        print(f"✅ System initialized in {init_time:.1f}ms")
        
        crisis_analyzer = managers.get('crisis_analyzer')
        if not crisis_analyzer:
            print("❌ CrisisAnalyzer not available")
            return
            
        # Performance test
        target_time = 500  # ms
        test_message = "I'm having a really difficult time and feeling overwhelmed with everything."
        num_runs = 10
        
        print(f"\n⚡ Running {num_runs} performance tests...")
        analysis_times = []
        
        for i in range(num_runs):
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
                    return
                    
                analysis_time = (time.time() - start_time) * 1000
                analysis_times.append(analysis_time)
                
                print(f"   Run {i+1}: {analysis_time:.1f}ms")
                
            except Exception as e:
                print(f"   ❌ Run {i+1} failed: {e}")
                
        if analysis_times:
            avg_time = statistics.mean(analysis_times)
            min_time = min(analysis_times)
            max_time = max(analysis_times)
            median_time = statistics.median(analysis_times)
            
            print("\n" + "=" * 80)
            print("📊 CRISIS ANALYSIS PERFORMANCE - CRITICAL METRICS")
            print("=" * 80)
            print(f"TARGET: {target_time}ms per analysis")
            print(f"AVERAGE: {avg_time:.1f}ms")
            print(f"MEDIAN: {median_time:.1f}ms")
            print(f"FASTEST: {min_time:.1f}ms")
            print(f"SLOWEST: {max_time:.1f}ms")
            
            if avg_time > target_time:
                gap = avg_time - target_time
                improvement_pct = ((avg_time / target_time) - 1) * 100
                print(f"PERFORMANCE GAP: {gap:.1f}ms over target")
                print(f"IMPROVEMENT NEEDED: {improvement_pct:.1f}% speed increase")
                
                print("\n🔧 OPTIMIZATION RECOMMENDATIONS:")
                if avg_time > 1500:
                    print("   - Consider model quantization or smaller models")
                    print("   - Implement aggressive result caching")
                elif avg_time > 1000:
                    print("   - Optimize GPU memory usage patterns")
                    print("   - Cache model inference results")
                elif avg_time > 750:
                    print("   - Cache frequently accessed patterns")
                    print("   - Optimize text preprocessing pipeline")
                else:
                    print("   - Fine-tune configuration access patterns")
                    print("   - Optimize helper class operations")
            else:
                print("🚀 PERFORMANCE: TARGET ACHIEVED!")
                
            print("=" * 80)
            
            # Return metrics for summary
            return {
                'avg_time_ms': avg_time,
                'target_ms': target_time,
                'improvement_needed_ms': max(0, avg_time - target_time),
                'improvement_needed_pct': ((avg_time / target_time) - 1) * 100 if avg_time > target_time else 0,
                'min_time_ms': min_time,
                'max_time_ms': max_time,
                'median_time_ms': median_time
            }
            
    except Exception as e:
        print(f"❌ Performance test failed: {e}")
        import traceback
        traceback.print_exc()
        return None

def test_configuration_performance(logger):
    """Test configuration access performance"""
    logger.info("🔧 Testing configuration access performance...")
    
    try:
        from managers.unified_config import create_unified_config_manager
        
        config = create_unified_config_manager()
        target_time = 10  # ms
        
        test_configs = [
            ('GLOBAL_LOG_LEVEL', 'INFO'),
            ('NLP_SERVER_HOST', '0.0.0.0'),
            ('GLOBAL_NLP_API_PORT', 8881),
            ('NLP_LOG_ENABLE_FILE_LOGGING', True),
            ('NLP_ANALYSIS_ENABLE_ENSEMBLE', True)
        ]
        
        print("\n⚙️ Testing configuration access speeds...")
        config_times = []
        
        for config_key, default_value in test_configs:
            try:
                start_time = time.time()
                
                if isinstance(default_value, bool):
                    value = config.get_env_bool(config_key, default_value)
                elif isinstance(default_value, int):
                    value = config.get_env_int(config_key, default_value)
                else:
                    value = config.get_env(config_key, default_value)
                    
                access_time = (time.time() - start_time) * 1000
                config_times.append(access_time)
                
                print(f"   {config_key}: {access_time:.3f}ms")
                
            except Exception as e:
                print(f"   ❌ {config_key} failed: {e}")
                
        if config_times:
            avg_time = statistics.mean(config_times)
            max_time = max(config_times)
            min_time = min(config_times)
            
            print("\n" + "=" * 60)
            print("📊 CONFIGURATION ACCESS PERFORMANCE")
            print("=" * 60)
            print(f"TARGET: <{target_time}ms per access")
            print(f"AVERAGE: {avg_time:.3f}ms")
            print(f"FASTEST: {min_time:.3f}ms")
            print(f"SLOWEST: {max_time:.3f}ms")
            print(f"CONFIGS TESTED: {len(config_times)}")
            
            if avg_time <= target_time:
                margin = target_time - avg_time
                print(f"🚀 EXCELLENT - {margin:.3f}ms under target")
            else:
                excess = avg_time - target_time
                print(f"⚠️ SLOW - {excess:.3f}ms over target")
                
            print("=" * 60)
            
            return {
                'avg_time_ms': avg_time,
                'target_ms': target_time,
                'min_time_ms': min_time,
                'max_time_ms': max_time
            }
            
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        return None

def main():
    """Main performance testing function"""
    logger = setup_logger()
    
    print("🌈" * 30)
    print("🚀 STANDALONE PERFORMANCE TEST")
    print("🏳️‍🌈 The Alphabet Cartel - Crisis Detection System")
    print("🌈" * 30)
    
    results = {}
    
    # Test 1: Configuration Performance
    print("\n📍 TEST 1: Configuration Access Performance")
    print("-" * 50)
    config_results = test_configuration_performance(logger)
    if config_results:
        results['configuration'] = config_results
    
    # Test 2: Crisis Analysis Performance
    print("\n📍 TEST 2: Crisis Analysis Performance")
    print("-" * 50)
    crisis_results = test_crisis_analysis_performance(logger)
    if crisis_results:
        results['crisis_analysis'] = crisis_results
    
    # Final Summary
    print("\n" + "🌈" * 30)
    print("📊 PERFORMANCE SUMMARY")
    print("🌈" * 30)
    
    if 'configuration' in results:
        config = results['configuration']
        print(f"\n⚙️ CONFIGURATION ACCESS:")
        print(f"   Target: <{config['target_ms']}ms")
        print(f"   Actual: {config['avg_time_ms']:.3f}ms")
        print(f"   Status: {'✅ GOOD' if config['avg_time_ms'] <= config['target_ms'] else '⚠️ NEEDS IMPROVEMENT'}")
    
    if 'crisis_analysis' in results:
        crisis = results['crisis_analysis']
        print(f"\n🚨 CRISIS ANALYSIS:")
        print(f"   Target: {crisis['target_ms']}ms")
        print(f"   Actual: {crisis['avg_time_ms']:.1f}ms")
        print(f"   Range: {crisis['min_time_ms']:.1f}ms - {crisis['max_time_ms']:.1f}ms")
        print(f"   Status: {'🚀 TARGET ACHIEVED' if crisis['avg_time_ms'] <= crisis['target_ms'] else '⚠️ NEEDS OPTIMIZATION'}")
        
        if crisis['improvement_needed_ms'] > 0:
            print(f"   Gap: {crisis['improvement_needed_ms']:.1f}ms too slow")
            print(f"   Improvement: {crisis['improvement_needed_pct']:.1f}% speed increase needed")
    
    print("\n🏳️‍🌈 Performance testing complete!")
    return results

if __name__ == '__main__':
    main()