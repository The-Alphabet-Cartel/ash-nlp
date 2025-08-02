#!/usr/bin/env python3
"""
JSON-Based Label Management Script for Ash NLP
Location: ash/ash-nlp/scripts/manage_labels.py

Easy testing and switching of zero-shot label configurations using JSON file
"""

import sys
import os
import requests
import json
from pathlib import Path
from typing import Dict, List, Any

# Add the parent directory to the path so we can import config
sys.path.append(str(Path(__file__).parent.parent))

try:
    from managers.zero_shot_manager import ZeroShotLabelsConfig, get_labels_config
except ImportError:
    print("❌ Could not import zero_shot_config. Make sure you're running from the correct directory.")
    sys.exit(1)

class JSONLabelManager:
    """Label management using JSON configuration file"""
    
    def __init__(self, nlp_server_url: str = "http://localhost:8881"):
        self.nlp_server_url = nlp_server_url
        self.config = get_labels_config()
        
        # Test phrases that were failing in your comprehensive test
        self.test_phrases = {
            'high_crisis_failed': [
                "I have the pills ready",
                "Found the rope, it's time", 
                "Loading the gun now",
                "This is my final message",
                "Goodbye cruel world",
                "Setting up to end everything",
                "Standing on the ledge",
                "Gun is loaded and ready"
            ],
            'high_crisis_passed': [
                "I want to kill myself",
                "Life isn't worth living anymore",
                "Going to kill myself after this",
                "Ready to jump off the bridge",
                "Writing my suicide note"
            ],
            'medium_crisis': [
                "I'm having a complete mental breakdown",
                "Can't stop crying for hours",
                "Everything is falling apart",
                "At my absolute breaking point"
            ],
            'low_crisis': [
                "Having a really rough day",
                "Feeling pretty down lately",
                "Work is stressing me out",
                "Been feeling off lately"
            ],
            'no_crisis': [
                "Going to the grocery store",
                "What's everyone having for dinner",
                "Thanks for all the help",
                "Happy Friday everyone"
            ]
        }
    
    def show_config_info(self):
        """Show comprehensive configuration information"""
        print("📋 Label Configuration Information")
        print("=" * 60)
        
        config_info = self.config.get_config_info()
        
        print(f"Version: {config_info.get('version', 'Unknown')}")
        print(f"Description: {config_info.get('description', 'No description')}")
        print(f"Total Label Sets: {config_info.get('total_label_sets', 0)}")
        print()
        
        # Current set info
        current = config_info.get('current_set', {})
        print(f"🎯 Current Label Set: {current.get('name', 'Unknown')}")
        if current.get('info'):
            info = current['info']
            print(f"   Description: {info.get('description', 'No description')}")
            print(f"   Optimized For: {info.get('optimized_for', 'Unknown')}")
            print(f"   Sensitivity: {info.get('sensitivity_level', 'Unknown')}")
            print(f"   Recommended: {'Yes' if info.get('recommended') else 'No'}")
            if info.get('label_counts'):
                print(f"   Label Counts: {info['label_counts']}")
        print()
    
    def list_available_label_sets(self):
        """List all available label sets with details"""
        print("🏷️ Available Label Sets")
        print("=" * 60)
        
        available_sets = self.config.get_available_label_sets()
        current_set = self.config.get_current_label_set_name()
        
        for label_set_name in available_sets:
            info = self.config.get_label_set_info(label_set_name)
            
            # Mark current set
            marker = "🎯 " if label_set_name == current_set else "📋 "
            recommend_marker = " ⭐" if info and info.recommended else ""
            
            print(f"{marker}{info.name if info else label_set_name}{recommend_marker}")
            if info:
                print(f"   Description: {info.description}")
                print(f"   Optimized For: {info.optimized_for}")
                print(f"   Sensitivity: {info.sensitivity_level}")
                if info.label_counts:
                    total = sum(info.label_counts.values())
                    print(f"   Labels: {info.label_counts} (Total: {total})")
            print()
    
    def show_label_set_details(self, label_set_name: str):
        """Show detailed labels for a specific set"""
        if label_set_name not in self.config.get_available_label_sets():
            print(f"❌ Unknown label set: {label_set_name}")
            print(f"Available sets: {', '.join(self.config.get_available_label_sets())}")
            return
        
        # Temporarily switch to show labels
        original_set = self.config.get_current_label_set_name()
        self.config.switch_label_set(label_set_name)
        
        try:
            labels = self.config.get_all_labels()
            info = self.config.get_label_set_info(label_set_name)
            
            print(f"🔍 Detailed Labels for: {info.name if info else label_set_name}")
            print("=" * 60)
            
            if info:
                print(f"Description: {info.description}")
                print(f"Optimized For: {info.optimized_for}")
                print(f"Sensitivity Level: {info.sensitivity_level}")
                print()
            
            for model_type, model_labels in labels.items():
                print(f"📊 {model_type.upper()} MODEL LABELS:")
                print("-" * 40)
                for i, label in enumerate(model_labels, 1):
                    # Truncate very long labels for readability
                    display_label = label if len(label) <= 100 else f"{label[:97]}..."
                    print(f"{i:2d}. {display_label}")
                print()
            
            # Show mapping rules if available
            if hasattr(self.config, 'current_mapping_rules') and self.config.current_mapping_rules:
                print("🗺️ MAPPING RULES:")
                print("-" * 40)
                for model, rules in self.config.current_mapping_rules.items():
                    print(f"\n{model.upper()}:")
                    for category, patterns in rules.items():
                        print(f"   {category}: {len(patterns)} patterns")
                        # Show first few patterns
                        for pattern in patterns[:3]:
                            print(f"      • {pattern}")
                        if len(patterns) > 3:
                            print(f"      ... and {len(patterns) - 3} more")
        
        finally:
            # Switch back to original set
            self.config.switch_label_set(original_set)
    
    def test_label_set_locally(self, label_set_name: str):
        """Test label set locally (without server) on sample phrases"""
        if label_set_name not in self.config.get_available_label_sets():
            print(f"❌ Unknown label set: {label_set_name}")
            return
        
        # Switch to test set
        original_set = self.config.get_current_label_set_name()
        self.config.switch_label_set(label_set_name)
        
        try:
            print(f"🧪 Local Testing of Label Set: {label_set_name}")
            print("=" * 60)
            
            info = self.config.get_label_set_info(label_set_name)
            if info:
                print(f"Description: {info.description}")
                print(f"Sensitivity: {info.sensitivity_level}")
                print()
            
            # Show the actual labels being used
            labels = self.config.get_all_labels()
            print("📋 LABELS IN USE:")
            for model, model_labels in labels.items():
                print(f"\n{model.upper()} ({len(model_labels)} labels):")
                for i, label in enumerate(model_labels[:3], 1):  # Show first 3
                    print(f"  {i}. {label[:80]}...")
                if len(model_labels) > 3:
                    print(f"  ... and {len(model_labels) - 3} more")
            
            # Test mapping functions with actual zero-shot labels (this is how they're designed to work)
            print(f"\n🗺️ MAPPING FUNCTION TESTS:")
            print("-" * 40)
            
            # Test with actual depression labels
            depression_labels = self.config.get_depression_labels()
            test_depression_labels = [
                depression_labels[0] if len(depression_labels) > 0 else "person actively expressing suicidal thoughts",
                depression_labels[2] if len(depression_labels) > 2 else "person with mild depression",
                depression_labels[-1] if len(depression_labels) > 0 else "person with stable mental health"
            ]
            
            for label in test_depression_labels:
                result = self.config.map_depression_label(label)
                print(f"Depression: '{label[:50]}...' → {result}")
            
            # Test with actual sentiment labels  
            sentiment_labels = self.config.get_sentiment_labels()
            if sentiment_labels:
                test_sent_label = sentiment_labels[0]
                result = self.config.map_sentiment_label(test_sent_label)
                print(f"Sentiment: '{test_sent_label[:50]}...' → {result}")
            
            # Test with actual distress labels
            distress_labels = self.config.get_emotional_distress_labels()
            if distress_labels:
                test_dist_label = distress_labels[0]
                result = self.config.map_distress_label(test_dist_label)
                print(f"Distress: '{test_dist_label[:50]}...' → {result}")
            
            # Show mapping rules if available
            print(f"\n🔧 MAPPING RULES STATUS:")
            if hasattr(self.config, 'current_mapping_rules') and self.config.current_mapping_rules:
                print("✅ Mapping rules loaded:")
                for model, rules in self.config.current_mapping_rules.items():
                    total_patterns = sum(len(patterns) for patterns in rules.values())
                    print(f"   {model}: {total_patterns} patterns across {len(rules)} categories")
            else:
                print("❌ No mapping rules found - this might be the issue!")
            
            print(f"\n💡 NOTE: Mapping functions work with zero-shot model outputs, not user input.")
            print(f"    To test with actual user input, use 'test-server' command.")
        
        finally:
            # Switch back
            self.config.switch_label_set(original_set)
    
    def test_label_set_with_server(self, label_set_name: str):
        """Test label set against NLP server"""
        if label_set_name not in self.config.get_available_label_sets():
            print(f"❌ Unknown label set: {label_set_name}")
            return
        
        print(f"🧪 Server Testing of Label Set: {label_set_name}")
        print("=" * 60)
        
        # Try to switch label set on server
        try:
            switch_response = requests.post(
                f"{self.nlp_server_url}/admin/labels/switch",
                json={"label_set": label_set_name},
                timeout=10
            )
            if switch_response.status_code == 200:
                print("✅ Successfully switched label set on server")
            else:
                print(f"⚠️ Could not switch label set on server: {switch_response.status_code}")
                return
        except requests.RequestException as e:
            print(f"❌ Server not available: {e}")
            return
        
        # Test phrases by category
        results = {'high_crisis': [], 'medium_crisis': [], 'low_crisis': [], 'no_crisis': []}
        
        for category, phrases in self.test_phrases.items():
            print(f"\n🔍 Testing {category.replace('_', ' ').title()}:")
            print("-" * 30)
            
            for phrase in phrases:
                try:
                    response = requests.post(
                        f"{self.nlp_server_url}/analyze",
                        json={"message": phrase},
                        timeout=30
                    )
                    
                    if response.status_code == 200:
                        result = response.json()
                        risk_level = result.get('risk_level', 'unknown')
                        confidence = result.get('confidence', 0.0)
                        
                        print(f"   '{phrase[:50]}...' → {risk_level} ({confidence:.3f})")
                        
                        # Categorize result
                        if risk_level in ['high', 'severe']:
                            results['high_crisis'].append(phrase)
                        elif risk_level in ['medium', 'moderate']:
                            results['medium_crisis'].append(phrase)
                        elif risk_level in ['low', 'mild']:
                            results['low_crisis'].append(phrase)
                        else:
                            results['no_crisis'].append(phrase)
                            
                    else:
                        print(f"   ❌ Server error: {response.status_code}")
                        
                except requests.RequestException as e:
                    print(f"   ❌ Request failed: {e}")
        
        # Print summary
        print(f"\n📊 TESTING SUMMARY:")
        print("-" * 30)
        for category, phrases in results.items():
            print(f"{category.replace('_', ' ').title()}: {len(phrases)} phrases")
        
        # Analyze failed high crisis cases
        failed_high_crisis = set(self.test_phrases['high_crisis_failed']) - set(results['high_crisis'])
        if failed_high_crisis:
            print(f"\n⚠️ MISSED HIGH CRISIS CASES ({len(failed_high_crisis)}):")
            for phrase in failed_high_crisis:
                print(f"   • {phrase}")
    
    def compare_label_sets(self, set1: str, set2: str, test_phrase: str):
        """Compare how two label sets handle the same phrase"""
        available_sets = self.config.get_available_label_sets()
        
        if set1 not in available_sets:
            print(f"❌ Unknown label set: {set1}")
            return
        if set2 not in available_sets:
            print(f"❌ Unknown label set: {set2}")
            return
        
        print(f"⚖️ Comparing Label Sets on: '{test_phrase}'")
        print("=" * 60)
        
        original_set = self.config.get_current_label_set_name()
        
        for label_set_name in [set1, set2]:
            print(f"\n📋 Testing with {label_set_name.upper()}:")
            
            # Switch label set
            self.config.switch_label_set(label_set_name)
            
            # Test locally first
            depression_result = self.config.map_depression_label(f"person saying: {test_phrase}")
            sentiment_result = self.config.map_sentiment_label(f"person expressing: {test_phrase}")
            distress_result = self.config.map_distress_label(f"person experiencing: {test_phrase}")
            
            print(f"   Local Mapping:")
            print(f"     Depression: {depression_result}")
            print(f"     Sentiment: {sentiment_result}")
            print(f"     Distress: {distress_result}")
            
            # Test with server if available
            try:
                # Switch server to this label set
                requests.post(
                    f"{self.nlp_server_url}/admin/labels/switch",
                    json={"label_set": label_set_name},
                    timeout=10
                )
                
                # Test phrase
                response = requests.post(
                    f"{self.nlp_server_url}/analyze",
                    json={"message": test_phrase},
                    timeout=30
                )
                
                if response.status_code == 200:
                    result = response.json()
                    print(f"   Server Result:")
                    print(f"     Risk Level: {result.get('risk_level', 'unknown')}")
                    print(f"     Confidence: {result.get('confidence', 0.0):.3f}")
                
            except requests.RequestException:
                print(f"   Server: Not available")
        
        # Switch back to original
        self.config.switch_label_set(original_set)
    
    def export_label_set(self, label_set_name: str, output_file: str = None):
        """Export a label set to JSON file"""
        if label_set_name not in self.config.get_available_label_sets():
            print(f"❌ Unknown label set: {label_set_name}")
            return
        
        # Switch to export set
        original_set = self.config.get_current_label_set_name()
        self.config.switch_label_set(label_set_name)
        
        try:
            export_data = {
                'exported_at': '2025-08-02T12:00:00Z',  # Would use datetime.utcnow()
                'label_set': label_set_name,
                'info': self.config.get_label_set_info(label_set_name).__dict__,
                'labels': self.config.get_all_labels(),
                'stats': self.config.get_current_stats()
            }
            
            if output_file is None:
                output_file = f"exported_{label_set_name}_{export_data['exported_at'][:10]}.json"
            
            # Ensure output directory exists
            output_path = Path(output_file)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, indent=2, ensure_ascii=False)
            
            print(f"✅ Exported {label_set_name} to: {output_path}")
            print(f"📊 Export includes {export_data['stats']['total_labels']} total labels")
        
        finally:
            self.config.switch_label_set(original_set)
    
    def validate_label_set(self, label_set_name: str):
        """Validate a label set configuration"""
        if label_set_name not in self.config.get_available_label_sets():
            print(f"❌ Unknown label set: {label_set_name}")
            return
        
        print(f"✅ Validating Label Set: {label_set_name}")
        print("=" * 50)
        
        # Switch to validation set
        original_set = self.config.get_current_label_set_name()
        self.config.switch_label_set(label_set_name)
        
        try:
            validation = {
                'issues': [],
                'warnings': [],
                'stats': {}
            }
            
            # Get labels and basic stats
            labels = self.config.get_all_labels()
            stats = self.config.get_current_stats()
            validation['stats'] = stats
            
            print(f"📊 Basic Statistics:")
            print(f"   Total Labels: {stats.get('total_labels', 0)}")
            print(f"   Model Counts: {stats.get('model_counts', {})}")
            print()
            
            # Validate each model has labels
            required_models = ['depression', 'sentiment', 'emotional_distress']
            for model in required_models:
                if model not in labels:
                    validation['issues'].append(f"Missing {model} model labels")
                elif len(labels[model]) == 0:
                    validation['issues'].append(f"No labels defined for {model} model")
                elif len(labels[model]) < 3:
                    validation['warnings'].append(f"Only {len(labels[model])} labels for {model} model (recommend 5+)")
                else:
                    print(f"✅ {model.title()} Model: {len(labels[model])} labels")
            
            # Check for empty labels
            for model, model_labels in labels.items():
                for i, label in enumerate(model_labels):
                    if not label.strip():
                        validation['issues'].append(f"Empty label at position {i+1} in {model} model")
                    elif len(label.strip()) < 10:
                        validation['warnings'].append(f"Very short label in {model} model: '{label[:20]}...'")
            
            # Test mapping functions if available
            if hasattr(self.config, 'current_mapping_rules') and self.config.current_mapping_rules:
                print(f"\n🗺️ Testing Mapping Rules:")
                test_phrases = [
                    "person actively expressing suicidal thoughts",
                    "person showing moderate depression", 
                    "person with stable mental health",
                    "person expressing overwhelming sadness",
                    "person feeling content and happy"
                ]
                
                for phrase in test_phrases:
                    try:
                        dep_result = self.config.map_depression_label(phrase)
                        sent_result = self.config.map_sentiment_label(phrase)
                        dist_result = self.config.map_distress_label(phrase)
                        print(f"   '{phrase[:30]}...' → D:{dep_result} S:{sent_result} T:{dist_result}")
                    except Exception as e:
                        validation['issues'].append(f"Mapping test failed for '{phrase[:20]}...': {e}")
            
            # Summary
            print(f"\n📋 Validation Summary:")
            if validation['issues']:
                print(f"❌ Issues Found ({len(validation['issues'])}):")
                for issue in validation['issues']:
                    print(f"   • {issue}")
            
            if validation['warnings']:
                print(f"⚠️ Warnings ({len(validation['warnings'])}):")
                for warning in validation['warnings']:
                    print(f"   • {warning}")
            
            if not validation['issues'] and not validation['warnings']:
                print("✅ No issues found - label set is valid!")
            elif not validation['issues']:
                print("✅ No critical issues - label set is usable with warnings")
            else:
                print("❌ Critical issues found - label set needs attention")
                
        finally:
            # Switch back to original
            self.config.switch_label_set(original_set)
    
    def benchmark_label_set(self, label_set_name: str):
        """Run comprehensive benchmark on a label set"""
        if label_set_name not in self.config.get_available_label_sets():
            print(f"❌ Unknown label set: {label_set_name}")
            return
        
        print(f"📊 Comprehensive Benchmark: {label_set_name}")
        print("=" * 60)
        
        # Switch to benchmark set on server
        try:
            switch_response = requests.post(
                f"{self.nlp_server_url}/admin/labels/switch",
                json={"label_set": label_set_name},
                timeout=10
            )
            if switch_response.status_code != 200:
                print(f"❌ Could not switch server to {label_set_name}")
                return
        except requests.RequestException as e:
            print(f"❌ Server not available: {e}")
            return
        
        # Test comprehensive categories
        all_results = {}
        total_tests = 0
        total_passed = 0
        
        for category, phrases in self.test_phrases.items():
            print(f"\n🔍 Testing {category.replace('_', ' ').title()} ({len(phrases)} phrases):")
            category_passed = 0
            
            for phrase in phrases:
                try:
                    response = requests.post(
                        f"{self.nlp_server_url}/analyze",
                        json={"message": phrase},
                        timeout=30
                    )
                    
                    if response.status_code == 200:
                        result = response.json()
                        risk_level = result.get('risk_level', 'unknown')
                        confidence = result.get('confidence', 0.0)
                        
                        # Determine if this is a "pass" based on expected vs actual
                        expected_high = 'high_crisis' in category
                        detected_high = risk_level in ['high', 'severe']
                        
                        if expected_high == detected_high:
                            category_passed += 1
                            total_passed += 1
                            status = "✅"
                        else:
                            status = "❌"
                        
                        total_tests += 1
                        print(f"   {status} '{phrase[:40]}...' → {risk_level} ({confidence:.3f})")
                        
                    else:
                        print(f"   ❌ Server error for '{phrase[:40]}...'")
                        
                except requests.RequestException as e:
                    print(f"   ❌ Request failed for '{phrase[:40]}...': {e}")
            
            # Category summary
            pass_rate = (category_passed / len(phrases)) * 100 if phrases else 0
            all_results[category] = {
                'passed': category_passed,
                'total': len(phrases),
                'pass_rate': pass_rate
            }
            print(f"   📊 {category}: {category_passed}/{len(phrases)} ({pass_rate:.1f}%)")
        
        # Overall summary
        overall_pass_rate = (total_passed / total_tests) * 100 if total_tests > 0 else 0
        
        print(f"\n📈 BENCHMARK RESULTS for {label_set_name}:")
        print("=" * 50)
        print(f"Overall Pass Rate: {overall_pass_rate:.1f}% ({total_passed}/{total_tests})")
        print()
        
        # Detailed breakdown
        for category, results in all_results.items():
            status = "✅" if results['pass_rate'] >= 80 else "⚠️" if results['pass_rate'] >= 60 else "❌"
            print(f"{status} {category.replace('_', ' ').title()}: {results['pass_rate']:.1f}%")
        
        # Critical analysis
        high_crisis_results = all_results.get('high_crisis_failed', {})
        if high_crisis_results:
            high_pass_rate = high_crisis_results['pass_rate']
            if high_pass_rate < 85:
                print(f"\n⚠️ CRITICAL: High crisis detection at {high_pass_rate:.1f}% (target: 95%+)")
                print("   Consider switching to 'safety_first' label set or tuning thresholds")
            else:
                print(f"\n✅ High crisis detection: {high_pass_rate:.1f}% (good)")
        
        # Recommendations
        print(f"\n💡 RECOMMENDATIONS:")
        if overall_pass_rate >= 85:
            print("   • Excellent performance - ready for production")
        elif overall_pass_rate >= 75:
            print("   • Good performance - consider minor tuning")
        elif overall_pass_rate >= 65:
            print("   • Moderate performance - review failed cases")
        else:
            print("   • Poor performance - try different label set")
        
        # Performance comparison hint
        if label_set_name != 'enhanced_crisis':
            print(f"   • Try benchmarking 'enhanced_crisis' for comparison")
        
        print(f"\n🔄 To switch back to another label set:")
        print(f"   curl -X POST {self.nlp_server_url}/admin/labels/switch -d '{{\"label_set\": \"current\"}}'")

def main():
    """Main CLI interface"""
    if len(sys.argv) < 2:
        print("🏷️ Ash NLP JSON Label Management Tool")
        print("=" * 50)
        print("Configuration file: config/label_config.json")
        print()
        print("Usage:")
        print("  python manage_labels.py info                         # Show config info")
        print("  python manage_labels.py list                         # List available label sets")
        print("  python manage_labels.py show <set_name>              # Show labels for set")
        print("  python manage_labels.py test-local <set_name>        # Test label mapping locally")
        print("  python manage_labels.py test-server <set_name>       # Test with NLP server")
        print("  python manage_labels.py compare <set1> <set2> <phrase>  # Compare sets")
        print("  python manage_labels.py export <set_name> [file]     # Export label set")
        print("  python manage_labels.py validate <set_name>          # Validate label set")
        print("  python manage_labels.py benchmark <set_name>         # Run comprehensive benchmark")
        print()
        print("Examples:")
        print("  python manage_labels.py test-server enhanced_crisis")
        print("  python manage_labels.py compare current enhanced_crisis 'I have the pills ready'")
        print("  python manage_labels.py export safety_first exported_safety.json")
        print("  python manage_labels.py benchmark enhanced_crisis")
        return
    
    manager = JSONLabelManager()
    command = sys.argv[1].lower()
    
    if command == "info":
        manager.show_config_info()
    
    elif command == "list":
        manager.list_available_label_sets()
    
    elif command == "show" and len(sys.argv) >= 3:
        manager.show_label_set_details(sys.argv[2])
    
    elif command == "test-local" and len(sys.argv) >= 3:
        manager.test_label_set_locally(sys.argv[2])
    
    elif command == "test-server" and len(sys.argv) >= 3:
        manager.test_label_set_with_server(sys.argv[2])
    
    elif command == "compare" and len(sys.argv) >= 5:
        phrase = " ".join(sys.argv[4:])
        manager.compare_label_sets(sys.argv[2], sys.argv[3], phrase)
    
    elif command == "export" and len(sys.argv) >= 3:
        output_file = sys.argv[3] if len(sys.argv) >= 4 else None
        manager.export_label_set(sys.argv[2], output_file)
    
    elif command == "validate" and len(sys.argv) >= 3:
        manager.validate_label_set(sys.argv[2])
    
    elif command == "benchmark" and len(sys.argv) >= 3:
        manager.benchmark_label_set(sys.argv[2])
    
    else:
        print("❌ Invalid command or missing arguments")
        print("Use 'python manage_labels.py' for usage help")

if __name__ == "__main__":
    main()