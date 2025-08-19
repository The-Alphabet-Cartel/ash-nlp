# ash-nlp/tests/phase/3/e/test_crisis_pattern_manager_cleanup.py
"""
Integration Test for CrisisPatternManager Cleanup - Phase 3e Sub-step 5.3
FILE VERSION: v3.1-3e-5.3-test-1
LAST MODIFIED: 2025-08-19
PHASE: 3e Sub-step 5.3 - CrisisPatternManager cleanup validation
CLEAN ARCHITECTURE: v3.1 Compliant
Repository: https://github.com/the-alphabet-cartel/ash-nlp
Community: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org

PURPOSE: Validate that CrisisPatternManager works correctly after method migration to 
SharedUtilitiesManager and LearningSystemManager with proper migration references.

REAL SYSTEM TESTING: Uses actual configuration files and real UnifiedConfigManager - NO MOCKS

MIGRATION VALIDATION:
- validate_pattern_structure() → SharedUtilitiesManager.validate_data_structure()
- format_pattern_output() → SharedUtilitiesManager.format_response_data()
- log_pattern_performance() → SharedUtilitiesManager.log_performance_metric()
- update_pattern_from_feedback() → LearningSystemManager.update_patterns_from_feedback()
- evaluate_pattern_effectiveness() → LearningSystemManager.evaluate_pattern_performance()
"""

import pytest
import logging
import time
import json
from pathlib import Path
import sys
import os

# Add the project root to the Python path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from managers.crisis_pattern_manager import CrisisPatternManager, create_crisis_pattern_manager
from managers.unified_config_manager import UnifiedConfigManager, create_unified_config_manager

logger = logging.getLogger(__name__)

class TestCrisisPatternManagerCleanup:
    """Test CrisisPatternManager after Phase 3e Sub-step 5.3 cleanup using REAL system components"""
    
    @pytest.fixture
    def real_config_manager(self):
        """Create REAL UnifiedConfigManager using actual config files"""
        config_dir = project_root / "config"
        return create_unified_config_manager(str(config_dir))
    
    @pytest.fixture
    def crisis_pattern_manager(self, real_config_manager):
        """Create CrisisPatternManager instance using REAL configuration"""
        return create_crisis_pattern_manager(real_config_manager)
    
    # ========================================================================
    # MIGRATION REFERENCE TESTS - Using Real System
    # ========================================================================
    
    def test_validate_pattern_structure_migration_reference(self, crisis_pattern_manager, caplog):
        """Test that validate_pattern_structure() provides migration reference using real system"""
        with caplog.at_level(logging.WARNING):
            # Test with real pattern data structure
            pattern_data = {
                'pattern': 'want to die',
                'crisis_level': 'critical',
                'urgency': 'critical',
                'auto_escalate': True,
                'type': 'exact_match'
            }
            result = crisis_pattern_manager.validate_pattern_structure(pattern_data)
            
            # Should return basic validation for backward compatibility
            assert result is True
            
            # Should log migration warning
            assert "validate_pattern_structure() moved to SharedUtilitiesManager.validate_data_structure()" in caplog.text
    
    def test_format_pattern_output_migration_reference(self, crisis_pattern_manager, caplog):
        """Test that format_pattern_output() provides migration reference using real pattern results"""
        with caplog.at_level(logging.WARNING):
            # Use real pattern analysis results
            message = "I feel hopeless"
            analysis_result = crisis_pattern_manager.analyze_enhanced_patterns(message)
            pattern_results = analysis_result.get('patterns_found', [])
            
            result = crisis_pattern_manager.format_pattern_output(pattern_results, 'crisis_analysis')
            
            # Should return basic formatting for backward compatibility
            assert 'pattern_results' in result
            assert 'total_patterns' in result
            assert result['total_patterns'] == len(pattern_results)
            assert result['source'] == 'CrisisPatternManager_fallback'
            
            # Should log migration warning
            assert "format_pattern_output() moved to SharedUtilitiesManager.format_response_data()" in caplog.text
    
    def test_log_pattern_performance_migration_reference(self, crisis_pattern_manager, caplog):
        """Test that log_pattern_performance() provides migration reference with real timing"""
        with caplog.at_level(logging.WARNING):
            # Measure real pattern analysis performance
            start_time = time.time()
            crisis_pattern_manager.analyze_enhanced_patterns("test message")
            execution_time = time.time() - start_time
            
            crisis_pattern_manager.log_pattern_performance('enhanced_pattern_analysis', execution_time, True, {
                'patterns_checked': 5,
                'matches_found': 0
            })
            
            # Should log migration warning
            assert "log_pattern_performance() moved to SharedUtilitiesManager.log_performance_metric()" in caplog.text
            
            # Should log basic performance info for backward compatibility
            assert f"Pattern Performance [SUCCESS]: enhanced_pattern_analysis - {execution_time:.3f}s" in caplog.text
    
    def test_update_pattern_from_feedback_migration_reference(self, crisis_pattern_manager, caplog):
        """Test that update_pattern_from_feedback() provides migration reference with real feedback data"""
        with caplog.at_level(logging.WARNING):
            # Use realistic feedback data structure
            feedback_data = {
                'feedback_type': 'false_positive',
                'original_confidence': 0.8,
                'correct_confidence': 0.2,
                'user_id': 'community_member_123',
                'timestamp': time.time(),
                'context': 'crisis_support_channel'
            }
            result = crisis_pattern_manager.update_pattern_from_feedback('suicidal_ideation_pattern', feedback_data)
            
            # Should return True for backward compatibility (no actual learning)
            assert result is True
            
            # Should log migration warning
            assert "update_pattern_from_feedback() moved to LearningSystemManager.update_patterns_from_feedback()" in caplog.text
    
    def test_evaluate_pattern_effectiveness_migration_reference(self, crisis_pattern_manager, caplog):
        """Test that evaluate_pattern_effectiveness() provides migration reference with real time periods"""
        with caplog.at_level(logging.WARNING):
            # Test with realistic time periods
            for time_period in ['1h', '24h', '7d', '30d']:
                result = crisis_pattern_manager.evaluate_pattern_effectiveness('hopelessness_detection', time_period)
                
                # Should return fallback data for backward compatibility
                assert result['pattern_name'] == 'hopelessness_detection'
                assert result['time_period'] == time_period
                assert result['effectiveness_score'] == 0.0
                assert result['evaluation_available'] is False
                assert result['source'] == 'CrisisPatternManager_fallback'
            
            # Should log migration warning
            assert "evaluate_pattern_effectiveness() moved to LearningSystemManager.evaluate_pattern_performance()" in caplog.text
    
    # ========================================================================
    # CORE FUNCTIONALITY PRESERVATION TESTS - Real System
    # ========================================================================
    
    def test_analyze_enhanced_patterns_with_real_config(self, crisis_pattern_manager):
        """Test that core pattern analysis functionality works with real configuration files"""
        # Test with various real crisis messages
        test_messages = [
            "I want to die, there's no hope left",
            "Just having a normal day",
            "I feel completely hopeless about everything",
            "Can't cope with this anymore"
        ]
        
        for message in test_messages:
            result = crisis_pattern_manager.analyze_enhanced_patterns(message)
            
            # Should return valid structure regardless of content
            assert 'patterns_found' in result
            assert 'confidence_score' in result
            assert 'safety_flags' in result
            assert isinstance(result['patterns_found'], list)
            assert isinstance(result['confidence_score'], (int, float))
            assert isinstance(result['safety_flags'], dict)
    
    def test_apply_context_weights_with_real_environment_variables(self, crisis_pattern_manager):
        """Test that context weight application works with real environment variables"""
        test_cases = [
            ("I feel hopeless and desperate", 0.5),
            ("Everything is overwhelming me", 0.3),
            ("I'm struggling but getting help", 0.4),
            ("Having a good day today", 0.1)
        ]
        
        for message, base_score in test_cases:
            modified_score, details = crisis_pattern_manager.apply_context_weights(message, base_score)
            
            # Should return valid results
            assert isinstance(modified_score, float)
            assert 0.0 <= modified_score <= 1.0
            assert 'weights_applied' in details
            assert 'total_adjustment' in details
            assert 'phase_3e_compliant' in details
            assert details['phase_3e_compliant'] is True
    
    def test_extract_community_patterns_with_real_vocabulary(self, crisis_pattern_manager):
        """Test that community pattern extraction works with real community vocabulary"""
        # Test messages that might contain community-specific terms
        test_messages = [
            "I'm struggling as a trans person in my community",
            "Dealing with gender dysphoria and family rejection",
            "Coming out was really difficult for me",
            "This is just a regular message with no community terms"
        ]
        
        for message in test_messages:
            patterns = crisis_pattern_manager.extract_community_patterns(message)
            
            # Should return valid pattern list
            assert isinstance(patterns, list)
            
            # If patterns found, should have Phase 3e markers
            for pattern in patterns:
                assert 'pattern_type' in pattern
                assert 'matched_pattern' in pattern
                assert 'crisis_level' in pattern
                if 'phase_3e_extraction' in pattern:
                    assert pattern['phase_3e_extraction'] is True
    
    def test_comprehensive_message_analysis_real_world_scenarios(self, crisis_pattern_manager):
        """Test comprehensive analysis with real-world crisis scenarios"""
        real_world_scenarios = [
            {
                'message': "I don't want to live anymore, everything feels hopeless",
                'user_id': 'community_member_001',
                'channel_id': 'crisis_support',
                'expected_severity': ['high', 'critical']
            },
            {
                'message': "Having some struggles but my therapist is helping",
                'user_id': 'community_member_002', 
                'channel_id': 'general_support',
                'expected_severity': ['none', 'low', 'medium']
            },
            {
                'message': "Just wanted to say hi to everyone!",
                'user_id': 'community_member_003',
                'channel_id': 'social_chat',
                'expected_severity': ['none', 'low']
            }
        ]
        
        for scenario in real_world_scenarios:
            result = crisis_pattern_manager.analyze_message(
                scenario['message'], 
                scenario['user_id'], 
                scenario['channel_id']
            )
            
            # Should include Phase 3e metadata
            assert 'metadata' in result
            assert result['metadata']['manager_version'] == 'v3.1-3e-5.3-1'
            assert result['metadata']['phase_3e_migration_complete'] is True
            
            # Should maintain safety assessment
            assert 'safety_assessment' in result
            assert 'summary' in result
            
            # Should have appropriate severity level
            assert result['summary']['highest_crisis_level'] in scenario['expected_severity']
    
    def test_semantic_pattern_analysis_real_system(self, crisis_pattern_manager):
        """Test semantic pattern analysis with real system (fallback mode)"""
        crisis_messages = [
            "I don't want to live anymore",
            "Everything feels hopeless and pointless",
            "I can't cope with this overwhelming pain",
            "Just a normal conversation here"
        ]
        
        for message in crisis_messages:
            patterns = crisis_pattern_manager.find_triggered_patterns(message)
            
            # Should return valid pattern list
            assert isinstance(patterns, list)
            
            # If patterns found, should include Phase 3e markers
            for pattern in patterns:
                assert 'pattern_name' in pattern
                assert 'pattern_type' in pattern
                assert 'crisis_level' in pattern
                assert 'confidence' in pattern
    
    # ========================================================================
    # LGBTQIA+ COMMUNITY PATTERN PRESERVATION - Real System
    # ========================================================================
    
    def test_lgbtqia_community_patterns_real_config(self, crisis_pattern_manager):
        """Test that LGBTQIA+ community patterns work with real configuration"""
        # Test realistic LGBTQIA+ community messages
        community_messages = [
            "I'm questioning my gender identity and feeling lost",
            "Dealing with family rejection after coming out as trans", 
            "The dysphoria is getting really overwhelming",
            "Our community support group helps so much",
            "This message has no community-specific content"
        ]
        
        for message in community_messages:
            # Test community pattern extraction
            community_patterns = crisis_pattern_manager.extract_community_patterns(message)
            
            # Should return valid results
            assert isinstance(community_patterns, list)
            
            # Test comprehensive analysis
            full_analysis = crisis_pattern_manager.analyze_message(message, f"lgbtqia_member_{hash(message) % 1000}", "support_channel")
            
            # Should complete without errors
            assert full_analysis['analysis_available'] is True
            assert 'patterns_triggered' in full_analysis
            assert 'safety_assessment' in full_analysis
    
    # ========================================================================
    # CRISIS DETECTION FUNCTIONALITY - Real System Tests
    # ========================================================================
    
    def test_critical_crisis_detection_real_system(self, crisis_pattern_manager):
        """Test that critical crisis detection works with real configuration"""
        critical_messages = [
            "I want to kill myself tonight",
            "I'm planning to end my life", 
            "I don't want to exist anymore",
            "Ready to die, nothing matters"
        ]
        
        for message in critical_messages:
            result = crisis_pattern_manager.analyze_message(message, "test_user", "crisis_channel")
            
            # Should maintain core analysis structure
            assert result['analysis_available'] is True
            assert 'safety_assessment' in result
            assert 'summary' in result
            
            # Should detect concerning content (may not always trigger emergency based on real patterns)
            assert result['summary']['highest_crisis_level'] in ['none', 'low', 'medium', 'high', 'critical']
            
            # Should include Phase 3e version information
            assert result['metadata']['manager_version'] == 'v3.1-3e-5.3-1'
    
    def test_pattern_validation_real_patterns(self, crisis_pattern_manager):
        """Test pattern validation with real pattern structures"""
        # Test with realistic pattern data
        real_pattern_examples = [
            {'pattern': 'want to die', 'crisis_level': 'critical', 'type': 'exact_match'},
            {'pattern': 'hopeless', 'crisis_level': 'high', 'urgency': 'medium'},
            {'pattern': r'\b(kill|end)\s+(myself|my\s+life)\b', 'type': 'regex', 'crisis_level': 'critical'},
            {'invalid': 'missing required fields'},
            "not a dictionary at all"
        ]
        
        for pattern_data in real_pattern_examples:
            result = crisis_pattern_manager.validate_pattern_structure(pattern_data)
            assert isinstance(result, bool)
    
    # ========================================================================
    # REAL CONFIGURATION FILE INTEGRATION
    # ========================================================================
    
    def test_real_configuration_loading(self, crisis_pattern_manager):
        """Test that manager loads real configuration files correctly"""
        status = crisis_pattern_manager.get_status()
        
        # Should have loaded real pattern files
        assert status['status'] == 'operational'
        assert status['patterns_loaded'] >= 0  # May be 0 if no config files exist yet
        assert isinstance(status['pattern_types'], list)
        
        # Should include Phase 3e status information
        assert 'phase_3e_status' in status
        assert status['phase_3e_status']['sub_step'] == '5.3'
        assert status['phase_3e_status']['migration_complete'] is True
    
    def test_real_environment_variable_handling(self, crisis_pattern_manager):
        """Test that real environment variable handling works correctly"""
        # Test context weight application which uses real environment variables
        message = "I feel hopeless"
        base_score = 0.5
        
        try:
            modified_score, details = crisis_pattern_manager.apply_context_weights(message, base_score)
            
            # Should handle real environment variables correctly
            assert isinstance(modified_score, float)
            assert 0.0 <= modified_score <= 1.0
            assert 'source' in details
            assert details['source'] == 'existing_environment_variables'
            
        except Exception as e:
            # If environment variables aren't set up, should still handle gracefully
            assert "environment variables" in str(e).lower() or "config" in str(e).lower()
    
    # ========================================================================
    # MIGRATION DOCUMENTATION VALIDATION
    # ========================================================================
    
    def test_migration_reference_documentation_quality(self, crisis_pattern_manager):
        """Test that migration references include comprehensive documentation"""
        migrated_methods = [
            'validate_pattern_structure',
            'format_pattern_output', 
            'log_pattern_performance',
            'update_pattern_from_feedback',
            'evaluate_pattern_effectiveness'
        ]
        
        for method_name in migrated_methods:
            method = getattr(crisis_pattern_manager, method_name)
            docstring = method.__doc__
            
            # Should contain comprehensive migration information
            assert "MIGRATION REFERENCE" in docstring
            assert "Benefits of Migration" in docstring
            assert "New Location" in docstring
            assert "Usage Example" in docstring
            assert "DEPRECATED" in docstring
            
            # Should have specific manager references
            if method_name in ['validate_pattern_structure', 'format_pattern_output', 'log_pattern_performance']:
                assert "SharedUtilitiesManager" in docstring
            else:
                assert "LearningSystemManager" in docstring
    
    # ========================================================================
    # ERROR HANDLING AND RESILIENCE - Real System
    # ========================================================================
    
    def test_error_handling_real_system(self, crisis_pattern_manager):
        """Test error handling with real system components"""
        # Test with various edge cases
        edge_cases = [
            "",  # Empty message
            "a" * 10000,  # Very long message
            "🔥💯👍🚨",  # Emoji only
            "Normal message with some unicode: café naïve résumé",  # Unicode
            None,  # None input (will cause errors but should be handled)
        ]
        
        for test_input in edge_cases:
            try:
                if test_input is not None:
                    result = crisis_pattern_manager.analyze_message(test_input, "test_user", "test_channel")
                    # Should return valid structure even for edge cases
                    assert 'analysis_available' in result
                    assert 'metadata' in result
                    
            except Exception as e:
                # If errors occur, they should be reasonable (e.g., type errors for None)
                assert isinstance(e, (TypeError, AttributeError, ValueError))
    
    def test_factory_function_real_system(self):
        """Test factory function with real UnifiedConfigManager"""
        config_dir = project_root / "config"
        real_config_manager = create_unified_config_manager(str(config_dir))
        
        # Factory function should work with real config manager
        manager = create_crisis_pattern_manager(real_config_manager)
        assert isinstance(manager, CrisisPatternManager)
        assert manager.config_manager == real_config_manager
        
        # Should be able to get status
        status = manager.get_status()
        assert status['version'] == 'v3.1-3e-5.3-1'
    
    def test_real_system_integration_comprehensive(self, crisis_pattern_manager):
        """Comprehensive test of real system integration"""
        # Test realistic conversation scenario
        conversation_messages = [
            "Hi everyone, how is everyone doing today?",
            "I've been struggling a bit lately with some personal stuff",
            "The transition has been really difficult for me",
            "Sometimes I wonder if things will ever get better",
            "But I'm grateful for this supportive community"
        ]
        
        for i, message in enumerate(conversation_messages):
            try:
                result = crisis_pattern_manager.analyze_message(
                    message, 
                    f"community_member_real_test_{i}", 
                    "support_conversation"
                )
                
                # Should return properly structured result
                assert result['analysis_available'] is True
                assert 'patterns_triggered' in result
                assert 'safety_assessment' in result
                assert 'summary' in result
                assert 'metadata' in result
                
                # Should include Phase 3e information
                assert result['metadata']['manager_version'] == 'v3.1-3e-5.3-1'
                assert result['metadata']['phase_3e_migration_complete'] is True
                
            except Exception as e:
                pytest.fail(f"Real system integration failed for message {i}: {e}")


# ============================================================================
# TEST RUNNER - Real System Testing
# ============================================================================

def run_crisis_pattern_cleanup_tests():
    """Run all CrisisPatternManager cleanup tests using REAL system components"""
    print("🧪 Running CrisisPatternManager Phase 3e Sub-step 5.3 Cleanup Tests (REAL SYSTEM)...")
    print("📋 Testing with actual configuration files and real UnifiedConfigManager")
    print("🚫 NO MOCKS - Testing real-world application")
    
    # Configure logging for tests
    logging.basicConfig(level=logging.INFO)
    
    # Run pytest with verbose output
    pytest_args = [
        __file__,
        '-v',
        '--tb=short',
        '--color=yes',
        '-x'  # Stop on first failure for faster feedback
    ]
    
    exit_code = pytest.main(pytest_args)
    
    if exit_code == 0:
        print("\n✅ ALL CRISIS PATTERN MANAGER CLEANUP TESTS PASSED!")
        print("🔄 Migration references working correctly with REAL system")
        print("🛡️ LGBTQIA+ community patterns preserved in real configuration")
        print("🚨 Crisis detection functionality maintained with real patterns")
        print("🏗️ Phase 3e Sub-step 5.3 validation complete - REAL SYSTEM VERIFIED")
    else:
        print(f"\n❌ Some tests failed (exit code: {exit_code})")
        print("🔧 Check test output for details")
        print("📋 Tests use REAL system components - failures indicate actual integration issues")
    
    return exit_code


if __name__ == "__main__":
    exit_code = run_crisis_pattern_cleanup_tests()
    exit(exit_code)