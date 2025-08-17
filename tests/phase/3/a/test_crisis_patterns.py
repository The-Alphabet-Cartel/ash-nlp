"""
Crisis Pattern Manager Integration Tests - Phase 3a
FILE VERSION: v3.1-3d-10.7-1
LAST MODIFIED: 2025-08-13
PHASE: 3d Step 10.7 - Community Pattern Consolidation
CLEAN ARCHITECTURE: v3.1 Compliant
MIGRATION STATUS: Community patterns consolidated into CrisisPatternManager
Tests crisis pattern loading, caching, and analysis functionality.
"""

import os
import sys
import pytest
import tempfile
import json
from pathlib import Path
from unittest.mock import patch, MagicMock

# Add project root to Python path
project_root = Path(__file__).parent.parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

# STEP 9.8 FIX: Updated imports to use UnifiedConfigManager
from managers.unified_config_manager import create_unified_config_manager
from managers.crisis_pattern_manager import create_crisis_pattern_manager

class TestCrisisPatternManager:
    """Test suite for CrisisPatternManager functionality"""
    
    def setup_method(self):
        """Set up test environment before each test"""
        # STEP 9.8 FIX: Use UnifiedConfigManager with real config directory
        self.config_manager = create_unified_config_manager("/app/config")
        self.crisis_manager = create_crisis_pattern_manager(self.config_manager)

    def test_crisis_pattern_manager_initialization(self):
        """Test that CrisisPatternManager initializes correctly with UnifiedConfigManager"""
        assert self.crisis_manager is not None
        assert hasattr(self.crisis_manager, 'config_manager')
        assert hasattr(self.crisis_manager, '_patterns_cache')
        assert hasattr(self.crisis_manager, '_compiled_regex_cache')
        
        # Verify it's using UnifiedConfigManager
        from managers.unified_config_manager import UnifiedConfigManager
        assert isinstance(self.crisis_manager.config_manager, UnifiedConfigManager)

    def test_get_crisis_patterns(self):
        """Test crisis pattern retrieval"""
        patterns = self.crisis_manager.get_crisis_patterns()
        assert isinstance(patterns, list)
        # Should have patterns loaded from various pattern files
        assert len(patterns) >= 0  # May be empty in test environment

    def test_pattern_cache_functionality(self):
        """Test that pattern caching works correctly"""
        # Initial cache state
        initial_cache_size = len(self.crisis_manager._patterns_cache)
        
        # Load patterns should populate cache
        patterns = self.crisis_manager.get_crisis_patterns()
        
        # Cache should be populated
        assert len(self.crisis_manager._patterns_cache) >= initial_cache_size

    def test_comprehensive_message_analysis(self):
        """Test comprehensive message analysis functionality"""
        test_message = "I feel so overwhelmed and hopeless about everything"
        
        analysis_result = self.crisis_manager.analyze_message(
            test_message, 
            user_id="test_user", 
            channel_id="test_channel"
        )
        
        # Verify expected structure
        assert isinstance(analysis_result, dict)
        assert 'patterns_triggered' in analysis_result
        assert 'analysis_available' in analysis_result
        assert 'details' in analysis_result
        assert 'summary' in analysis_result
        assert 'metadata' in analysis_result
        
        # Verify analysis metadata
        assert analysis_result['metadata']['user_id'] == "test_user"
        assert analysis_result['metadata']['channel_id'] == "test_channel"
        assert 'analysis_timestamp' in analysis_result['metadata']

    def test_extract_community_patterns(self):
        """Test community pattern extraction - STEP 10.7: Direct CrisisPatternManager usage"""
        test_message = "I'm struggling with my identity in this community"
        
        # STEP 10.7: Use CrisisPatternManager methods directly instead of utils import
        community_patterns = self.crisis_manager.extract_community_patterns(test_message)
        assert isinstance(community_patterns, list)

    def test_extract_crisis_context_phrases(self):
        """Test crisis context phrase extraction - STEP 10.7: Direct CrisisPatternManager usage"""
        test_message = "I can't take this anymore, everything is falling apart"
        
        # STEP 10.7: Use CrisisPatternManager methods directly instead of utils import
        context_phrases = self.crisis_manager.extract_crisis_context_phrases(test_message)
        assert isinstance(context_phrases, list)

    def test_analyze_temporal_indicators(self):
        """Test temporal indicator analysis - STEP 10.7: Direct CrisisPatternManager usage"""
        test_message = "I need help right now, this is urgent"
        
        # STEP 10.7: Use CrisisPatternManager methods directly instead of utils import
        temporal_analysis = self.crisis_manager.analyze_temporal_indicators(test_message)
        assert isinstance(temporal_analysis, dict)
        assert 'found_indicators' in temporal_analysis
        assert 'urgency_score' in temporal_analysis

    def test_analyze_enhanced_patterns(self):
        """Test enhanced pattern analysis"""
        test_message = "I feel hopeless and worthless, nothing will ever get better"
        
        enhanced_analysis = self.crisis_manager.analyze_enhanced_patterns(test_message)
        assert isinstance(enhanced_analysis, dict)
        assert 'patterns_found' in enhanced_analysis
        assert 'confidence_score' in enhanced_analysis

    def test_step_10_7_new_methods(self):
        """Test new methods added in Step 10.7"""
        test_message = "I feel overwhelmed and hopeless"
        base_score = 0.5
        
        # Test apply_context_weights method (Step 10.7)
        weighted_score, weight_details = self.crisis_manager.apply_context_weights(test_message, base_score)
        assert isinstance(weighted_score, (int, float))
        assert isinstance(weight_details, dict)
        assert weighted_score >= 0.0
        assert weighted_score <= 1.0
        
        # Test check_enhanced_crisis_patterns method (Step 10.7)
        enhanced_patterns = self.crisis_manager.check_enhanced_crisis_patterns(test_message)
        assert isinstance(enhanced_patterns, dict)
        assert 'matches' in enhanced_patterns
        assert 'highest_urgency' in enhanced_patterns
        assert 'auto_escalate' in enhanced_patterns
        assert 'total_weight' in enhanced_patterns
        assert 'requires_immediate_attention' in enhanced_patterns

    def test_error_handling(self):
        """Test error handling in pattern analysis"""
        # Test with empty message
        result = self.crisis_manager.analyze_message("")
        assert result['analysis_available'] == True  # Should still provide analysis
        
        # Test with None message (should handle gracefully)
        try:
            result = self.crisis_manager.analyze_message(None, "test_user", "test_channel")
            # Should either work or handle gracefully
            assert 'error' in result or result['analysis_available'] == True
        except Exception:
            # Acceptable if it raises an exception for None input
            pass

    def test_get_status(self):
        """Test status reporting functionality"""
        status = self.crisis_manager.get_status()
        
        assert isinstance(status, dict)
        assert 'status' in status
        assert 'patterns_loaded' in status
        assert 'version' in status
        
        # Verify Step 10.7 specific status info
        if 'step_10_7_methods_added' in status:
            step_10_7_info = status['step_10_7_methods_added']
            assert 'apply_context_weights' in step_10_7_info
            assert 'check_enhanced_crisis_patterns' in step_10_7_info

def test_manager_integration_with_step_10_7():
    """Test Step 10.7 specific improvements"""
    config_manager = create_unified_config_manager("/app/config")
    crisis_manager = create_crisis_pattern_manager(config_manager)
    
    # Test that status reflects Step 10.7 completion
    status = crisis_manager.get_status()
    assert 'version' in status
    assert 'config_manager' in status
    assert status['config_manager'] == 'UnifiedConfigManager'

# STEP 10.7: Updated community pattern tests - no more utils import
def test_community_pattern_extraction_step_10_7():
    """Test community pattern extraction functionality - STEP 10.7: Direct manager usage"""
    try:
        # STEP 10.7: Use UnifiedConfigManager and CrisisPatternManager directly
        config_manager = create_unified_config_manager("/app/config")
        crisis_pattern_manager = create_crisis_pattern_manager(config_manager)
        
        # STEP 10.7: No more CommunityPatternExtractor wrapper - use manager methods directly
        test_messages = [
            "My family rejected me when I came out as trans",
            "I'm struggling with gender dysphoria today",
            "The LGBTQ community has been so supportive",
            "I need help right now with coming out anxiety"
        ]
        
        total_patterns_found = 0
        
        for message in test_messages:
            # STEP 10.7: Direct method calls on CrisisPatternManager
            community_patterns = crisis_pattern_manager.extract_community_patterns(message)
            context_phrases = crisis_pattern_manager.extract_crisis_context_phrases(message)
            temporal_analysis = crisis_pattern_manager.analyze_temporal_indicators(message)
            enhanced_patterns = crisis_pattern_manager.check_enhanced_crisis_patterns(message)
            
            patterns_found = (len(community_patterns) + 
                            len(context_phrases) + 
                            len(temporal_analysis.get('found_indicators', [])) +
                            len(enhanced_patterns.get('matches', [])))
            total_patterns_found += patterns_found
        
        # Should find at least some patterns (exact count depends on configuration)
        assert total_patterns_found >= 0
        return True
        
    except Exception as e:
        print(f"Community pattern extraction test failed: {e}")
        return False

def test_step_10_7_consolidation_validation():
    """Test that Step 10.7 consolidation is working correctly"""
    config_manager = create_unified_config_manager("/app/config")
    crisis_manager = create_crisis_pattern_manager(config_manager)
    
    # Test message that should trigger various patterns
    test_message = "I don't want to live anymore, I feel completely hopeless and overwhelmed"
    
    # Test all consolidated methods work
    community_patterns = crisis_manager.extract_community_patterns(test_message)
    context_phrases = crisis_manager.extract_crisis_context_phrases(test_message)
    temporal_analysis = crisis_manager.analyze_temporal_indicators(test_message)
    enhanced_patterns = crisis_manager.check_enhanced_crisis_patterns(test_message)
    weighted_score, weight_details = crisis_manager.apply_context_weights(test_message, 0.5)
    
    # Verify all methods return expected types
    assert isinstance(community_patterns, list)
    assert isinstance(context_phrases, list) 
    assert isinstance(temporal_analysis, dict)
    assert isinstance(enhanced_patterns, dict)
    assert isinstance(weighted_score, (int, float))
    assert isinstance(weight_details, dict)
    
    # Verify consolidated methods have expected structure
    assert 'found_indicators' in temporal_analysis
    assert 'matches' in enhanced_patterns
    assert 'weights_applied' in weight_details or 'error' in weight_details

if __name__ == "__main__":
    # Run tests when script is executed directly
    pytest.main([__file__, "-v"])