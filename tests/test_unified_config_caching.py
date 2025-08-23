# tests/test_unified_config_caching.py
"""
UnifiedConfigManager Caching Performance Validation Test
Phase 3e Step 7 - Performance Optimization Validation

This test validates that the caching enhancement provides the expected performance improvements
while maintaining 100% functional compatibility with existing behavior.
"""

import time
import unittest
import os
import tempfile
import json
from pathlib import Path

# Import the enhanced UnifiedConfigManager
from managers.unified_config import create_unified_config_manager

class TestUnifiedConfigManagerCaching(unittest.TestCase):
    """Test caching functionality of UnifiedConfigManager"""
    
    @classmethod
    def setUpClass(cls):
        """Set up test environment with temporary config files"""
        cls.test_dir = tempfile.mkdtemp()
        cls.config_dir = Path(cls.test_dir) / "config"
        cls.config_dir.mkdir(parents=True)
        
        # Create test configuration files
        cls._create_test_config_files()
        
        # Enable caching for tests
        os.environ['NLP_PERFORMANCE_ENABLE_CONFIG_CACHING'] = 'true'
        os.environ['NLP_CONFIG_CACHE_TTL_SECONDS'] = '600'  # 10 minutes for tests
        
    @classmethod
    def _create_test_config_files(cls):
        """Create test configuration files"""
        # Create analysis_config.json
        analysis_config = {
            "algorithm_parameters": {
                "ensemble_weights": [0.4, 0.3, 0.3],
                "confidence_threshold": 0.5,
                "timeout_seconds": 30.0
            },
            "crisis_thresholds": {
                "low": 0.12,
                "medium": 0.25,
                "high": 0.45,
                "critical": 0.7
            }
        }
        with open(cls.config_dir / "analysis_config.json", 'w') as f:
            json.dump(analysis_config, f)
        
        # Create model_coordination.json
        model_config = {
            "ensemble_config": {
                "mode": "consensus",
                "gap_detection": True
            },
            "hardware_settings": {
                "device": "auto",
                "precision": "float16"
            }
        }
        with open(cls.config_dir / "model_coordination.json", 'w') as f:
            json.dump(model_config, f)
    
    @classmethod
    def tearDownClass(cls):
        """Clean up test environment"""
        import shutil
        shutil.rmtree(cls.test_dir)
        
        # Clean up environment variables
        if 'NLP_PERFORMANCE_ENABLE_CONFIG_CACHING' in os.environ:
            del os.environ['NLP_PERFORMANCE_ENABLE_CONFIG_CACHING']
        if 'NLP_CONFIG_CACHE_TTL_SECONDS' in os.environ:
            del os.environ['NLP_CONFIG_CACHE_TTL_SECONDS']
    
    def setUp(self):
        """Set up test case"""
        self.manager = create_unified_config_manager(str(self.config_dir))
    
    def test_caching_enabled(self):
        """Test that caching is properly enabled"""
        self.assertTrue(hasattr(self.manager, '_caching_enabled'))
        self.assertTrue(self.manager._caching_enabled)
        self.assertIsNotNone(self.manager.caching_helper)
        
        status = self.manager.get_status()
        self.assertIn('caching', status)
        self.assertTrue(status['caching']['enabled'])
    
    def test_cache_performance_improvement(self):
        """Test that caching provides measurable performance improvement"""
        config_name = 'analysis_config'
        section_path = 'algorithm_parameters'
        
        # Clear cache to ensure clean test
        self.manager.clear_configuration_cache()
        
        # First access (cache miss) - should be slower
        start_time = time.time()
        result1 = self.manager.get_config_section(config_name, section_path)
        first_access_time = (time.time() - start_time) * 1000  # Convert to milliseconds
        
        # Second access (cache hit) - should be faster
        start_time = time.time()
        result2 = self.manager.get_config_section(config_name, section_path)
        second_access_time = (time.time() - start_time) * 1000
        
        # Third access (cache hit) - should also be fast
        start_time = time.time()
        result3 = self.manager.get_config_section(config_name, section_path)
        third_access_time = (time.time() - start_time) * 1000
        
        # Verify results are identical
        self.assertEqual(result1, result2)
        self.assertEqual(result2, result3)
        
        # Verify performance improvement (cache should be at least 5x faster)
        self.assertLess(second_access_time, first_access_time / 5,
                       f"Cache hit ({second_access_time:.3f}ms) should be much faster than miss ({first_access_time:.3f}ms)")
        self.assertLess(third_access_time, first_access_time / 5,
                       f"Subsequent cache hit ({third_access_time:.3f}ms) should be much faster than miss ({first_access_time:.3f}ms)")
        
        print(f"Cache performance test:")
        print(f"  First access (miss): {first_access_time:.3f}ms")
        print(f"  Second access (hit): {second_access_time:.3f}ms")
        print(f"  Third access (hit): {third_access_time:.3f}ms")
        print(f"  Performance improvement: {first_access_time / second_access_time:.1f}x faster")
    
    def test_cache_statistics_tracking(self):
        """Test that cache statistics are properly tracked"""
        # Clear cache and stats
        self.manager.clear_configuration_cache()
        
        # Perform several accesses
        for i in range(5):
            self.manager.get_config_section('analysis_config', 'algorithm_parameters')
            self.manager.get_config_section('model_coordination', 'ensemble_config')
        
        # Check statistics
        stats = self.manager.get_cache_statistics()
        
        self.assertTrue(stats['enabled'])
        self.assertGreater(stats['total_requests'], 0)
        self.assertGreater(stats['cache_hits'], 0)
        self.assertGreater(stats['hit_rate'], 0)
        self.assertGreater(stats['current_entries'], 0)
        self.assertGreater(stats['performance_improvement'], 1.0)  # Should be faster than 1x
        
        print(f"Cache statistics after test:")
        print(f"  Total requests: {stats['total_requests']}")
        print(f"  Hit rate: {stats['hit_rate']:.1f}%")
        print(f"  Cache entries: {stats['current_entries']}")
        print(f"  Memory usage: {stats['memory_usage_mb']:.2f}MB")
        print(f"  Performance improvement: {stats['performance_improvement']:.1f}x")
    
    def test_cache_invalidation_on_file_change(self):
        """Test that cache invalidates when files are modified - FIXED VERSION"""
        config_name = 'analysis_config'
        section_path = 'algorithm_parameters'
        
        # Clear cache
        self.manager.clear_configuration_cache()
        
        # First access to populate cache
        result1 = self.manager.get_config_section(config_name, section_path)
        original_threshold = result1['confidence_threshold']
        
        # Verify it's cached
        stats_before = self.manager.get_cache_statistics()
        self.assertGreater(stats_before['current_entries'], 0, "Cache should have entries after first access")
        
        # FIXED: Add a small delay to ensure file modification time difference
        import time
        time.sleep(0.2)  # 200ms delay to ensure mtime difference
        
        # Modify the file (update modification time and content)
        config_path = self.config_dir / "analysis_config.json"
        
        # Read current content
        with open(config_path, 'r') as f:
            content = json.load(f)
        
        # Modify the content meaningfully
        new_threshold = 0.75 if original_threshold != 0.75 else 0.85
        content['algorithm_parameters']['confidence_threshold'] = new_threshold
        
        # Write back with explicit file sync to ensure mtime update
        with open(config_path, 'w') as f:
            json.dump(content, f)
            f.flush()
            os.fsync(f.fileno())  # Force filesystem sync
        
        # FIXED: Add another small delay to ensure mtime propagation  
        time.sleep(0.1)
        
        # Verify file was actually modified
        import os
        new_mtime = os.path.getmtime(config_path)
        
        # Access again - should detect file change and reload
        result2 = self.manager.get_config_section(config_name, section_path)
        new_loaded_threshold = result2['confidence_threshold']
        
        # Debug information
        print(f"Cache invalidation test debug:")
        print(f"  Original threshold: {original_threshold}")
        print(f"  Modified threshold: {new_threshold}")
        print(f"  Reloaded threshold: {new_loaded_threshold}")
        print(f"  File mtime: {new_mtime}")
        
        # Verify the change was detected
        self.assertNotEqual(original_threshold, new_loaded_threshold, 
                           f"Cache should have detected file change. Original: {original_threshold}, Loaded: {new_loaded_threshold}")
        self.assertEqual(new_loaded_threshold, new_threshold,
                        f"Loaded value should match file content. Expected: {new_threshold}, Got: {new_loaded_threshold}")
        
        print("  ✓ Cache correctly invalidated on file change")
    
    def test_backward_compatibility(self):
        """Test that all existing API methods work unchanged"""
        # Test all the main methods that managers use
        
        # get_config_section
        result1 = self.manager.get_config_section('analysis_config', 'algorithm_parameters')
        self.assertIsNotNone(result1)
        self.assertIn('ensemble_weights', result1)
        
        # load_config_file  
        result2 = self.manager.load_config_file('model_coordination')
        self.assertIsNotNone(result2)
        self.assertIn('ensemble_config', result2)
        
        # get_status
        status = self.manager.get_status()
        self.assertEqual(status['status'], 'operational')
        self.assertIn('caching', status)
        
        # Environment variable methods
        test_value = self.manager.get_env_str('TEST_VAR', 'default_value')
        self.assertEqual(test_value, 'default_value')
        
        print("✅ All backward compatibility tests passed")
    
    def test_multiple_manager_instances(self):
        """Test that multiple manager instances can coexist with caching"""
        # Create multiple managers
        manager1 = create_unified_config_manager(str(self.config_dir))
        manager2 = create_unified_config_manager(str(self.config_dir))
        
        # Both should have caching enabled
        self.assertTrue(manager1._caching_enabled)
        self.assertTrue(manager2._caching_enabled)
        
        # Both should be able to load configurations
        result1 = manager1.get_config_section('analysis_config', 'algorithm_parameters')
        result2 = manager2.get_config_section('analysis_config', 'algorithm_parameters')
        
        # Results should be identical
        self.assertEqual(result1, result2)
        
        print("✅ Multiple manager instances work correctly with caching")
    
    def test_cache_with_disabled_caching(self):
        """Test behavior when caching is disabled"""
        # Temporarily disable caching
        os.environ['NLP_PERFORMANCE_ENABLE_CONFIG_CACHING'] = 'false'
        
        try:
            manager_no_cache = create_unified_config_manager(str(self.config_dir))
            
            # Should not have caching enabled
            self.assertFalse(manager_no_cache._caching_enabled)
            self.assertIsNone(manager_no_cache.caching_helper)
            
            # But should still work normally
            result = manager_no_cache.get_config_section('analysis_config', 'algorithm_parameters')
            self.assertIsNotNone(result)
            self.assertIn('ensemble_weights', result)
            
            # Cache statistics should show disabled
            stats = manager_no_cache.get_cache_statistics()
            self.assertFalse(stats['enabled'])
            
            print("✅ Disabled caching works correctly")
            
        finally:
            # Re-enable caching
            os.environ['NLP_PERFORMANCE_ENABLE_CONFIG_CACHING'] = 'true'

def run_caching_performance_benchmark():
    """Run a comprehensive performance benchmark of the caching system - FIXED VERSION"""
    print("\n" + "="*70)
    print("UNIFIED CONFIG MANAGER CACHING PERFORMANCE BENCHMARK")
    print("="*70)
    
    # Create temporary test environment
    test_dir = tempfile.mkdtemp()
    config_dir = Path(test_dir) / "config"
    config_dir.mkdir(parents=True)
    
    try:
        # FIXED: Create test config with the exact same structure as real configs
        test_config = {
            "test_section": {
                "param1": "value1",
                "param2": 42,
                "param3": [1, 2, 3, 4, 5],
                "nested": {
                    "deep_param": "deep_value"
                }
            },
            "performance_test": {
                "iterations": 100,
                "data_size": "medium"
            }
        }
        with open(config_dir / "analysis_config.json", 'w') as f:  # Use existing config name
            json.dump(test_config, f)
        
        # Enable caching
        os.environ['NLP_PERFORMANCE_ENABLE_CONFIG_CACHING'] = 'true'
        
        # Create managers
        print("\n🚀 Creating UnifiedConfigManager with caching enabled...")
        cached_manager = create_unified_config_manager(str(config_dir))
        
        print("📊 Running performance benchmark...")
        
        # Benchmark parameters
        num_tests = 50  # Reduced for cleaner output
        config_name = 'analysis_config'  # Use existing config name
        section_path = 'test_section'
        
        # Clear cache for clean test
        cached_manager.clear_configuration_cache()
        
        # Test cache misses (first access)
        print(f"\n📈 Testing {num_tests} cache misses (first-time access)...")
        miss_times = []
        for i in range(num_tests):
            # Clear cache before each access to force miss
            cached_manager.clear_configuration_cache()
            
            start_time = time.time()
            result = cached_manager.get_config_section(config_name, section_path)
            access_time = (time.time() - start_time) * 1000
            miss_times.append(access_time)
            
            # Verify we got valid data
            if not result:
                print(f"Warning: Empty result on iteration {i}")
        
        avg_miss_time = sum(miss_times) / len(miss_times)
        
        # Test cache hits (subsequent access) 
        print(f"⚡ Testing {num_tests} cache hits (cached access)...")
        hit_times = []
        
        # First access to populate cache
        cached_manager.get_config_section(config_name, section_path)
        
        for i in range(num_tests):
            start_time = time.time()
            result = cached_manager.get_config_section(config_name, section_path)
            access_time = (time.time() - start_time) * 1000
            hit_times.append(access_time)
            
            # Verify we got valid data
            if not result:
                print(f"Warning: Empty cached result on iteration {i}")
        
        avg_hit_time = sum(hit_times) / len(hit_times)
        
        # Calculate performance improvement
        performance_improvement = avg_miss_time / avg_hit_time if avg_hit_time > 0 else 1.0
        
        # Get final cache statistics
        final_stats = cached_manager.get_cache_statistics()
        
        # Display results
        print(f"\n📊 PERFORMANCE BENCHMARK RESULTS:")
        print(f"{'='*50}")
        print(f"Average cache miss time:  {avg_miss_time:.3f}ms")
        print(f"Average cache hit time:   {avg_hit_time:.4f}ms")
        print(f"Performance improvement:  {performance_improvement:.1f}x faster")
        print(f"Time saved per hit:       {avg_miss_time - avg_hit_time:.3f}ms")
        
        print(f"\n📈 CACHE STATISTICS:")
        print(f"Hit rate:                {final_stats['hit_rate']:.1f}%")
        print(f"Total requests:          {final_stats['total_requests']}")
        print(f"Cache entries:           {final_stats['current_entries']}")
        print(f"Memory usage:            {final_stats['memory_usage_mb']:.2f}MB")
        print(f"Cache efficiency:        {final_stats['cache_efficiency']}")
        
        # Projected system-wide impact
        print(f"\n🎯 PROJECTED SYSTEM-WIDE IMPACT:")
        if avg_miss_time > 0.1:  # If cache misses are > 0.1ms
            config_calls_per_analysis = 5  # Estimate for typical analysis
            time_saved_per_analysis = (avg_miss_time - avg_hit_time) * config_calls_per_analysis
            print(f"Config calls per analysis: ~{config_calls_per_analysis}")
            print(f"Time saved per analysis:   ~{time_saved_per_analysis:.2f}ms")
            print(f"Contribution to 79ms goal: {(time_saved_per_analysis / 79) * 100:.1f}%")
            
            if time_saved_per_analysis >= 10:
                print(f"🎉 EXCELLENT: Caching provides significant contribution to performance target!")
            elif time_saved_per_analysis >= 5:
                print(f"✓ GOOD: Caching provides meaningful performance improvement")
            else:
                print(f"📝 NOTE: Caching provides modest but measurable improvement")
        
        print(f"\n✅ CACHING PERFORMANCE VALIDATION COMPLETE")
        return True
        
    finally:
        # Clean up
        import shutil
        shutil.rmtree(test_dir)
        if 'NLP_PERFORMANCE_ENABLE_CONFIG_CACHING' in os.environ:
            del os.environ['NLP_PERFORMANCE_ENABLE_CONFIG_CACHING']

if __name__ == '__main__':
    # Run the test suite
    print("Running UnifiedConfigManager Caching Tests...")
    unittest.main(verbosity=2, exit=False)
    
    # Run performance benchmark
    run_caching_performance_benchmark()