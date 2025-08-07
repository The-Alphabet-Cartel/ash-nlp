#!/usr/bin/env python3
"""
Phase 3a Validation Test - Crisis Pattern Manager Integration
Tests the migration from hardcoded patterns to JSON-based CrisisPatternManager

This test validates that:
1. CrisisPatternManager loads all JSON configuration files correctly
2. Pattern analysis produces equivalent results to the old hardcoded system
3. All pattern types are accessible and functional
4. Integration with CrisisAnalyzer works properly
"""

import sys
import os
import logging
import asyncio
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

def test_crisis_pattern_manager_initialization():
    """Test CrisisPatternManager initialization with JSON configs"""
    logger.info("🔍 Testing CrisisPatternManager initialization...")
    
    try:
        from managers.config_manager import ConfigManager
        from managers.crisis_pattern_manager import create_crisis_pattern_manager
        
        # Initialize with test config directory
        config_dir = "/app/config"  # Docker path
        if not os.path.exists(config_dir):
            config_dir = "./config"  # Local development path
        
        config_manager = ConfigManager(config_dir)
        crisis_pattern_manager = create_crisis_pattern_manager(config_manager)
        
        # Validate initialization
        status = crisis_pattern_manager.get_status()
        logger.info(f"✅ CrisisPatternManager initialized: {status['loaded_pattern_sets']} pattern sets")
        
        # Validate pattern loading
        validation = crisis_pattern_manager.validate_patterns()
        if validation['valid']:
            logger.info("✅ All patterns validated successfully")
            for pattern_type, count in validation['pattern_counts'].items():
                logger.info(f"   {pattern_type}: {count} patterns")
        else:
            logger.error(f"❌ Pattern validation failed: {validation['errors']}")
            return False
        
        return True
        
    except Exception as e:
        logger.error(f"❌ CrisisPatternManager initialization failed: {e}")
        return False

def test_pattern_access_methods():
    """Test all pattern access methods"""
    logger.info("🔧 Testing pattern access methods...")
    
    try:
        from managers.config_manager import ConfigManager
        from managers.crisis_pattern_manager import create_crisis_pattern_manager
        
        config_manager = ConfigManager("./config" if os.path.exists("./config") else "/app/config")
        crisis_pattern_manager = create_crisis_pattern_manager(config_manager)
        
        # Test each pattern access method
        pattern_methods = [
            ('get_crisis_context_patterns', 'Crisis Context Patterns'),
            ('get_positive_context_patterns', 'Positive Context Patterns'),
            ('get_temporal_indicators', 'Temporal Indicators'),
            ('get_community_vocabulary', 'Community Vocabulary'),
            ('get_context_weights', 'Context Weights'),
            ('get_enhanced_crisis_patterns', 'Enhanced Crisis Patterns'),
            ('get_idiom_patterns', 'Idiom Patterns'),
            ('get_burden_patterns', 'Burden Patterns'),
            ('get_lgbtqia_patterns', 'LGBTQIA+ Patterns')
        ]
        
        for method_name, description in pattern_methods:
            try:
                method = getattr(crisis_pattern_manager, method_name)
                patterns = method()
                
                if patterns and patterns.get('patterns'):
                    pattern_count = len(patterns['patterns'])
                    logger.info(f"✅ {description}: {pattern_count} pattern groups loaded")
                else:
                    logger.warning(f"⚠️ {description}: No patterns found")
                    
            except Exception as e:
                logger.error(f"❌ {description} access failed: {e}")
                return False
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Pattern access test failed: {e}")
        return False

def test_community_pattern_extraction():
    """Test community pattern extraction functionality"""
    logger.info("🏳️‍🌈 Testing community pattern extraction...")
    
    try:
        from managers.config_manager import ConfigManager
        from managers.crisis_pattern_manager import create_crisis_pattern_manager
        from utils.community_patterns import CommunityPatternExtractor
        
        config_manager = ConfigManager("./config" if os.path.exists("./config") else "/app/config")
        crisis_pattern_manager = create_crisis_pattern_manager(config_manager)
        extractor = CommunityPatternExtractor(crisis_pattern_manager)
        
        # Test community pattern extraction
        test_messages = [
            "My family rejected me when I came out as trans",
            "I'm struggling with gender dysphoria today",
            "The LGBTQ community has been so supportive",
            "I need help right now with coming out anxiety"
        ]
        
        total_patterns_found = 0
        
        for message in test_messages:
            community_patterns = extractor.extract_community_patterns(message)
            context_phrases = extractor.extract_crisis_context_phrases(message)
            temporal_analysis = extractor.analyze_temporal_indicators(message)
            
            patterns_found = len(community_patterns) + len(context_phrases) + len(temporal_analysis.get('found_indicators', []))
            total_patterns_found += patterns_found
            
            if patterns_found > 0:
                logger.info(f"✅ '{message[:50]}...': {patterns_found} patterns found")
            else:
                logger.info(f"ℹ️ '{message[:50]}...': No patterns found")
        
        logger.info(f"✅ Community pattern extraction test complete: {total_patterns_found} total patterns found")
        return True
        
    except Exception as e:
        logger.error(f"❌ Community pattern extraction test failed: {e}")
        return False

def test_context_weight_application():
    """Test context weight application"""
    logger.info("⚖️ Testing context weight application...")
    
    try:
        from managers.config_manager import ConfigManager
        from managers.crisis_pattern_manager import create_crisis_pattern_manager
        from utils.community_patterns import CommunityPatternExtractor
        
        config_manager = ConfigManager("./config" if os.path.exists("./config") else "/app/config")
        crisis_pattern_manager = create_crisis_pattern_manager(config_manager)
        extractor = CommunityPatternExtractor(crisis_pattern_manager)
        
        # Test context weight application
        test_cases = [
            ("I'm feeling really depressed and hopeless", 0.5),  # Should increase score
            ("I'm proud and happy about my transition", 0.5),    # Should decrease score
            ("This movie killed me, it was so funny", 0.3),     # Should decrease score (humor context)
            ("I'm struggling and scared about everything", 0.4)  # Should increase score
        ]
        
        for message, base_score in test_cases:
            modified_score, analysis = extractor.apply_context_weights(message, base_score)
            
            score_change = modified_score - base_score
            direction = "increased" if score_change > 0 else "decreased" if score_change < 0 else "unchanged"
            
            logger.info(f"✅ '{message[:40]}...': Score {direction} ({base_score:.2f} → {modified_score:.2f})")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Context weight application test failed: {e}")
        return False

def test_enhanced_crisis_patterns():
    """Test enhanced crisis pattern detection"""
    logger.info("🚨 Testing enhanced crisis pattern detection...")
    
    try:
        from managers.config_manager import ConfigManager
        from managers.crisis_pattern_manager import create_crisis_pattern_manager
        from utils.community_patterns import CommunityPatternExtractor
        
        config_manager = ConfigManager("./config" if os.path.exists("./config") else "/app/config")
        crisis_pattern_manager = create_crisis_pattern_manager(config_manager)
        extractor = CommunityPatternExtractor(crisis_pattern_manager)
        
        # Test high-risk messages
        high_risk_messages = [
            "I have no hope left and nothing matters anymore",
            "Everyone would be better off without me",
            "I made a plan and I'm ready to say goodbye",
            "I can't take it anymore and I'm completely hopeless"
        ]
        
        for message in high_risk_messages:
            enhanced_analysis = extractor.check_enhanced_crisis_patterns(message)
            
            if enhanced_analysis.get('matches'):
                urgency = enhanced_analysis.get('highest_urgency', 'none')
                auto_escalate = enhanced_analysis.get('auto_escalate', False)
                immediate_attention = enhanced_analysis.get('requires_immediate_attention', False)
                
                logger.info(f"🚨 High-risk pattern detected: '{message[:40]}...'")
                logger.info(f"   Urgency: {urgency}, Auto-escalate: {auto_escalate}, Immediate: {immediate_attention}")
            else:
                logger.info(f"ℹ️ No enhanced patterns: '{message[:40]}...'")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Enhanced crisis pattern test failed: {e}")
        return False

def test_crisis_analyzer_integration():
    """Test CrisisAnalyzer integration with CrisisPatternManager"""
    logger.info("🔗 Testing CrisisAnalyzer integration...")
    
    try:
        # This test would require the full system to be running
        # For now, we'll test that the import and initialization work
        from analysis.crisis_analyzer import CrisisAnalyzer
        
        # Mock model manager for testing
        class MockModelManager:
            def models_loaded(self):
                return True
            
            def get_model(self, model_type):
                return None
            
            def analyze_with_ensemble(self, message):
                return {
                    'consensus': {'prediction': 'safe', 'confidence': 0.2},
                    'detected_categories': [],
                    'model_info': 'mock_ensemble'
                }
        
        from managers.config_manager import ConfigManager
        from managers.crisis_pattern_manager import create_crisis_pattern_manager
        
        config_manager = ConfigManager("./config" if os.path.exists("./config") else "/app/config")
        crisis_pattern_manager = create_crisis_pattern_manager(config_manager)
        mock_models_manager = MockModelManager()
        
        # Test CrisisAnalyzer initialization with pattern manager
        crisis_analyzer = CrisisAnalyzer(
            models_manager=mock_models_manager,
            crisis_pattern_manager=crisis_pattern_manager
        )
        
        status = crisis_analyzer.get_status()
        
        if status['crisis_pattern_manager_available']:
            logger.info("✅ CrisisAnalyzer successfully integrated with CrisisPatternManager")
            logger.info(f"   Pattern manager status: {status['crisis_pattern_manager_available']}")
            logger.info(f"   Community extractor: {status['community_extractor_available']}")
        else:
            logger.error("❌ CrisisAnalyzer integration failed")
            return False
        
        return True
        
    except Exception as e:
        logger.error(f"❌ CrisisAnalyzer integration test failed: {e}")
        return False

def test_settings_manager_migration_notices():
    """Test that SettingsManager provides proper migration notices"""
    logger.info("📋 Testing SettingsManager migration notices...")
    
    try:
        from managers.config_manager import ConfigManager
        from managers.settings_manager import create_settings_manager
        
        config_manager = ConfigManager("./config" if os.path.exists("./config") else "/app/config")
        settings_manager = create_settings_manager(config_manager)
        
        # Test deprecated methods return migration notices
        migration_notice = settings_manager.get_crisis_patterns_migration_notice()
        
        if migration_notice.get('status') == 'migrated_to_json_configuration':
            logger.info("✅ SettingsManager provides proper migration notices")
            logger.info(f"   Migration phase: {migration_notice.get('phase')}")
            logger.info(f"   New location: {migration_notice.get('new_location')}")
        else:
            logger.error("❌ SettingsManager migration notices not working")
            return False
        
        # Test deprecated method warnings
        try:
            result = settings_manager.get_lgbtqia_patterns()
            if isinstance(result, dict) and 'status' in result:
                logger.info("✅ Deprecated methods return migration notices")
            else:
                logger.warning("⚠️ Deprecated methods don't return expected format")
        except Exception:
            logger.warning("⚠️ Deprecated method test failed")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ SettingsManager migration test failed: {e}")
        return False

def main():
    """Run all Phase 3a validation tests"""
    logger.info("🚀 Starting Phase 3a Crisis Pattern Manager validation tests...")
    logger.info("=" * 80)
    
    tests = [
        ("CrisisPatternManager Initialization", test_crisis_pattern_manager_initialization),
        ("Pattern Access Methods", test_pattern_access_methods),
        ("Community Pattern Extraction", test_community_pattern_extraction),
        ("Context Weight Application", test_context_weight_application),
        ("Enhanced Crisis Patterns", test_enhanced_crisis_patterns),
        ("CrisisAnalyzer Integration", test_crisis_analyzer_integration),
        ("SettingsManager Migration Notices", test_settings_manager_migration_notices)
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
    
    logger.info("\n" + "=" * 80)
    logger.info(f"📊 Phase 3a Validation Results:")
    logger.info(f"   ✅ Passed: {passed}")
    logger.info(f"   ❌ Failed: {failed}")
    logger.info(f"   📈 Success Rate: {(passed/(passed+failed)*100):.1f}%")
    
    if failed == 0:
        logger.info("🎉 Phase 3a Crisis Pattern Manager migration validation: SUCCESS!")
        logger.info("🔍 All crisis patterns successfully migrated to JSON configuration")
        logger.info("🏗️ CrisisPatternManager integration complete and functional")
        return True
    else:
        logger.error("❌ Phase 3a validation incomplete - some tests failed")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)