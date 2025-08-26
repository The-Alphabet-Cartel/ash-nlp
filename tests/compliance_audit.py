# Phase 3e Step 8.2: Streamlined Architecture Compliance Audit
# Focus: Clean Architecture v3.1 Rules 1-4 Validation

"""
Ash-NLP Phase 3e Step 8.2: Architecture Compliance Audit
========================================================
Repository: https://github.com/the-alphabet-cartel/ash-nlp
Community: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org

AUDIT SCOPE: Clean Architecture v3.1 Rules 1-4
RATIONALE: Rules 5-7 validated through Phase 3e execution and manual line-by-line audit

STATUS: Ready for execution
TARGET: Final architecture validation for Phase 3e completion
"""

import os
import re
import ast
from typing import Dict, List, Tuple, Any
from pathlib import Path

class Phase3eArchitectureAudit:
    """
    Streamlined architecture compliance audit for Phase 3e completion
    
    Validates Clean Architecture v3.1 Rules 1-4:
    - Rule 1: Dependency Direction
    - Rule 2: Factory Function Pattern  
    - Rule 3: Single Responsibility
    - Rule 4: Configuration Access
    """
    
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root)
        self.managers_dir = self.project_root / "managers"
        self.analysis_dir = self.project_root / "analysis"
        
        # Phase 3e manager inventory
        self.phase_3e_managers = [
            "analysis_config_manager.py",
            "crisis_threshold_manager.py", 
            "feature_config_manager.py",
            "learning_system_manager.py",
            "logging_config_manager.py",
            "model_coordination_manager.py",
            "pattern_detection_manager.py",
            "performance_config_manager.py",
            "pydantic_manager.py",
            "server_config_manager.py",
            "settings_manager.py",
            "shared_utilities_manager.py",
            "storage_config_manager.py",
            "unified_config_manager.py",
            "zero_shot_manager.py"
        ]
        
        self.audit_results = {
            'rule_1_dependency_direction': {},
            'rule_2_factory_functions': {},
            'rule_3_single_responsibility': {},
            'rule_4_configuration_access': {},
            'overall_compliance': 0.0,
            'violations': [],
            'recommendations': []
        }
    
    def execute_full_audit(self) -> Dict[str, Any]:
        """Execute complete streamlined architecture audit"""
        print("Phase 3e Step 8.2: Architecture Compliance Audit")
        print("=" * 50)
        print(f"Auditing {len(self.phase_3e_managers)} managers against Clean v3.1 Rules 1-4")
        print()
        
        # Execute rule-by-rule validation
        self._audit_rule_1_dependency_direction()
        self._audit_rule_2_factory_functions()
        self._audit_rule_3_single_responsibility() 
        self._audit_rule_4_configuration_access()
        
        # Calculate overall compliance
        self._calculate_overall_compliance()
        
        # Generate final report
        self._generate_audit_report()
        
        return self.audit_results
    
    def _audit_rule_1_dependency_direction(self):
        """Audit Rule 1: Dependency Direction (Infrastructure -> Business Logic)"""
        print("Auditing Rule 1: Dependency Direction")
        print("-" * 40)
        
        rule_1_results = {
            'compliant_managers': [],
            'violations': [],
            'dependency_flow': {},
            'score': 0.0
        }
        
        for manager_file in self.phase_3e_managers:
            manager_path = self.managers_dir / manager_file
            if not manager_path.exists():
                continue
                
            manager_name = manager_file.replace('.py', '')
            dependencies = self._extract_manager_dependencies(manager_path)
            
            # Check dependency direction
            violations = []
            for dep in dependencies:
                if self._is_outward_dependency(dep):
                    violations.append(f"Outward dependency: {dep}")
            
            if violations:
                rule_1_results['violations'].append({
                    'manager': manager_name,
                    'violations': violations
                })
            else:
                rule_1_results['compliant_managers'].append(manager_name)
            
            rule_1_results['dependency_flow'][manager_name] = dependencies
        
        # Calculate Rule 1 score
        total_managers = len(self.phase_3e_managers)
        compliant_count = len(rule_1_results['compliant_managers'])
        rule_1_results['score'] = (compliant_count / total_managers) * 100
        
        self.audit_results['rule_1_dependency_direction'] = rule_1_results
        print(f"Rule 1 Compliance: {rule_1_results['score']:.1f}% ({compliant_count}/{total_managers})")
        print()
    
    def _audit_rule_2_factory_functions(self):
        """Audit Rule 2: Factory Function Pattern"""
        print("Auditing Rule 2: Factory Function Pattern")
        print("-" * 40)
        
        rule_2_results = {
            'compliant_managers': [],
            'violations': [],
            'factory_functions': {},
            'score': 0.0
        }
        
        for manager_file in self.phase_3e_managers:
            manager_path = self.managers_dir / manager_file
            if not manager_path.exists():
                continue
                
            manager_name = manager_file.replace('.py', '')
            factory_info = self._check_factory_function(manager_path, manager_name)
            
            if factory_info['compliant']:
                rule_2_results['compliant_managers'].append(manager_name)
            else:
                rule_2_results['violations'].append({
                    'manager': manager_name,
                    'issues': factory_info['issues']
                })
            
            rule_2_results['factory_functions'][manager_name] = factory_info
        
        # Calculate Rule 2 score
        total_managers = len(self.phase_3e_managers)
        compliant_count = len(rule_2_results['compliant_managers'])
        rule_2_results['score'] = (compliant_count / total_managers) * 100
        
        self.audit_results['rule_2_factory_functions'] = rule_2_results
        print(f"Rule 2 Compliance: {rule_2_results['score']:.1f}% ({compliant_count}/{total_managers})")
        print()
    
    def _audit_rule_3_single_responsibility(self):
        """Audit Rule 3: Single Responsibility Principle"""
        print("Auditing Rule 3: Single Responsibility")
        print("-" * 40)
        
        rule_3_results = {
            'compliant_managers': [],
            'violations': [],
            'responsibility_analysis': {},
            'score': 0.0
        }
        
        # Define expected responsibilities based on Phase 3e design
        expected_responsibilities = {
            'unified_config_manager': 'Configuration management and environment variable access',
            'crisis_threshold_manager': 'Crisis level threshold determination',
            'model_coordination_manager': 'AI model coordination and ensemble management',
            'pattern_detection_manager': 'Crisis pattern detection and matching',
            'analysis_config_manager': 'Analysis parameter configuration',
            'shared_utilities_manager': 'Shared utility methods and common functionality',
            'learning_system_manager': 'Learning and adaptation system management',
            'feature_config_manager': 'Feature flag and toggle management',
            'pydantic_manager': 'Data model definitions and validation',
            'performance_config_manager': 'Performance configuration settings',
            'logging_config_manager': 'Logging configuration and setup',
            'server_config_manager': 'Server configuration management',
            'settings_manager': 'Application settings coordination',
            'storage_config_manager': 'Storage configuration management',
            'zero_shot_manager': 'Zero-shot classification label management'
        }
        
        for manager_file in self.phase_3e_managers:
            manager_path = self.managers_dir / manager_file
            if not manager_path.exists():
                continue
                
            manager_name = manager_file.replace('.py', '')
            responsibility_check = self._analyze_single_responsibility(
                manager_path, 
                manager_name,
                expected_responsibilities.get(manager_name, 'Unknown responsibility')
            )
            
            if responsibility_check['compliant']:
                rule_3_results['compliant_managers'].append(manager_name)
            else:
                rule_3_results['violations'].append({
                    'manager': manager_name,
                    'issues': responsibility_check['issues']
                })
            
            rule_3_results['responsibility_analysis'][manager_name] = responsibility_check
        
        # Calculate Rule 3 score
        total_managers = len(self.phase_3e_managers)
        compliant_count = len(rule_3_results['compliant_managers'])
        rule_3_results['score'] = (compliant_count / total_managers) * 100
        
        self.audit_results['rule_3_single_responsibility'] = rule_3_results
        print(f"Rule 3 Compliance: {rule_3_results['score']:.1f}% ({compliant_count}/{total_managers})")
        print()
    
    def _audit_rule_4_configuration_access(self):
        """Audit Rule 4: Configuration Access via UnifiedConfigManager"""
        print("Auditing Rule 4: Configuration Access")
        print("-" * 40)
        
        rule_4_results = {
            'compliant_managers': [],
            'violations': [],
            'config_patterns': {},
            'score': 0.0
        }
        
        for manager_file in self.phase_3e_managers:
            manager_path = self.managers_dir / manager_file
            if not manager_path.exists():
                continue
                
            manager_name = manager_file.replace('.py', '')
            
            # Skip UnifiedConfigManager itself
            if manager_name == 'unified_config_manager':
                rule_4_results['compliant_managers'].append(manager_name)
                rule_4_results['config_patterns'][manager_name] = {
                    'compliant': True,
                    'reason': 'Core configuration manager - exempt from this rule'
                }
                continue
            
            config_check = self._check_configuration_access(manager_path, manager_name)
            
            if config_check['compliant']:
                rule_4_results['compliant_managers'].append(manager_name)
            else:
                rule_4_results['violations'].append({
                    'manager': manager_name,
                    'issues': config_check['issues']
                })
            
            rule_4_results['config_patterns'][manager_name] = config_check
        
        # Calculate Rule 4 score
        total_managers = len(self.phase_3e_managers)
        compliant_count = len(rule_4_results['compliant_managers'])
        rule_4_results['score'] = (compliant_count / total_managers) * 100
        
        self.audit_results['rule_4_configuration_access'] = rule_4_results
        print(f"Rule 4 Compliance: {rule_4_results['score']:.1f}% ({compliant_count}/{total_managers})")
        print()
    
    def _extract_manager_dependencies(self, manager_path: Path) -> List[str]:
        """Extract dependencies from manager file"""
        dependencies = []
        try:
            with open(manager_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract import statements
            import_patterns = [
                r'from\s+([a-zA-Z_][a-zA-Z0-9_\.]*)\s+import',
                r'import\s+([a-zA-Z_][a-zA-Z0-9_\.]*)',
            ]
            
            for pattern in import_patterns:
                matches = re.findall(pattern, content)
                dependencies.extend(matches)
            
            # Filter to relevant dependencies
            relevant_deps = []
            for dep in dependencies:
                if any(keyword in dep for keyword in ['managers', 'analysis', 'config']):
                    relevant_deps.append(dep)
            
            return relevant_deps
            
        except Exception as e:
            return []
    
    def _is_outward_dependency(self, dependency: str) -> bool:
        """Check if dependency points outward (violates Rule 1)"""
        # In clean architecture, these would be outward dependencies:
        outward_indicators = [
            'api.',      # API layer depending on infrastructure
            'web.',      # Web layer depending on external
            'external.', # External service dependencies
            'database.', # Direct database dependencies
        ]
        
        for indicator in outward_indicators:
            if indicator in dependency:
                return True
        return False
    
    def _check_factory_function(self, manager_path: Path, manager_name: str) -> Dict[str, Any]:
        """Check if manager has proper factory function"""
        try:
            with open(manager_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            expected_factory = f"create_{manager_name}"
            
            # Check for factory function existence
            if expected_factory in content:
                # Check for proper factory pattern
                factory_pattern = rf'def\s+{expected_factory}\s*\([^)]*\):'
                if re.search(factory_pattern, content):
                    return {
                        'compliant': True,
                        'factory_function': expected_factory,
                        'issues': []
                    }
                else:
                    return {
                        'compliant': False,
                        'factory_function': expected_factory,
                        'issues': ['Factory function exists but pattern is incorrect']
                    }
            else:
                return {
                    'compliant': False,
                    'factory_function': expected_factory,
                    'issues': [f'Missing factory function: {expected_factory}']
                }
                
        except Exception as e:
            return {
                'compliant': False,
                'factory_function': f"create_{manager_name}",
                'issues': [f'Error reading file: {str(e)}']
            }
    
    def _analyze_single_responsibility(self, manager_path: Path, manager_name: str, expected_responsibility: str) -> Dict[str, Any]:
        """Analyze if manager adheres to single responsibility principle"""
        try:
            with open(manager_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Count public methods (rough indicator of responsibility scope)
            method_pattern = r'def\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\('
            methods = re.findall(method_pattern, content)
            public_methods = [m for m in methods if not m.startswith('_')]
            
            # Analyze method naming for coherence
            method_prefixes = {}
            for method in public_methods:
                prefix = method.split('_')[0] if '_' in method else method[:4]
                method_prefixes[prefix] = method_prefixes.get(prefix, 0) + 1
            
            # Determine compliance based on method count and coherence
            issues = []
            if len(public_methods) > 15:
                issues.append(f"High method count ({len(public_methods)}) may indicate multiple responsibilities")
            
            if len(method_prefixes) > 5:
                issues.append(f"Diverse method prefixes ({list(method_prefixes.keys())}) may indicate mixed concerns")
            
            return {
                'compliant': len(issues) == 0,
                'expected_responsibility': expected_responsibility,
                'method_count': len(public_methods),
                'method_prefixes': method_prefixes,
                'issues': issues
            }
            
        except Exception as e:
            return {
                'compliant': False,
                'expected_responsibility': expected_responsibility,
                'issues': [f'Error analyzing file: {str(e)}']
            }
    
    def _check_configuration_access(self, manager_path: Path, manager_name: str) -> Dict[str, Any]:
        """Check if manager properly accesses configuration via UnifiedConfigManager"""
        try:
            with open(manager_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            issues = []
            
            # Check for direct os.getenv usage (violation)
            if 'os.getenv' in content or 'os.environ' in content:
                issues.append('Direct os.getenv/os.environ usage detected')
            
            # Check for UnifiedConfigManager dependency
            if 'UnifiedConfigManager' not in content and 'config_manager' not in content:
                issues.append('No UnifiedConfigManager dependency found')
            
            # Check for get_config_section usage (Phase 3e pattern)
            if 'get_config_section' not in content:
                # Allow some managers to not use this pattern
                exempted_managers = ['pydantic_manager', 'settings_manager']
                if manager_name not in exempted_managers:
                    issues.append('No get_config_section() usage found (Phase 3e pattern)')
            
            return {
                'compliant': len(issues) == 0,
                'uses_unified_config': 'UnifiedConfigManager' in content,
                'uses_get_config_section': 'get_config_section' in content,
                'has_direct_env_access': 'os.getenv' in content or 'os.environ' in content,
                'issues': issues
            }
            
        except Exception as e:
            return {
                'compliant': False,
                'issues': [f'Error checking configuration access: {str(e)}']
            }
    
    def _calculate_overall_compliance(self):
        """Calculate overall compliance score across all rules"""
        rule_scores = [
            self.audit_results['rule_1_dependency_direction']['score'],
            self.audit_results['rule_2_factory_functions']['score'],
            self.audit_results['rule_3_single_responsibility']['score'],
            self.audit_results['rule_4_configuration_access']['score']
        ]
        
        self.audit_results['overall_compliance'] = sum(rule_scores) / len(rule_scores)
    
    def _generate_audit_report(self):
        """Generate comprehensive audit report"""
        print("PHASE 3E STEP 8.2 AUDIT RESULTS")
        print("=" * 50)
        print()
        
        print("CLEAN ARCHITECTURE v3.1 COMPLIANCE SUMMARY:")
        print(f"Rule 1 (Dependency Direction): {self.audit_results['rule_1_dependency_direction']['score']:.1f}%")
        print(f"Rule 2 (Factory Functions): {self.audit_results['rule_2_factory_functions']['score']:.1f}%")
        print(f"Rule 3 (Single Responsibility): {self.audit_results['rule_3_single_responsibility']['score']:.1f}%")
        print(f"Rule 4 (Configuration Access): {self.audit_results['rule_4_configuration_access']['score']:.1f}%")
        print()
        print(f"OVERALL COMPLIANCE: {self.audit_results['overall_compliance']:.1f}%")
        print()
        
        # Show violations if any
        all_violations = []
        for rule_key in ['rule_1_dependency_direction', 'rule_2_factory_functions', 
                        'rule_3_single_responsibility', 'rule_4_configuration_access']:
            violations = self.audit_results[rule_key].get('violations', [])
            for violation in violations:
                all_violations.append({
                    'rule': rule_key.replace('rule_', 'Rule ').replace('_', ' ').title(),
                    'manager': violation['manager'],
                    'issues': violation.get('issues', violation.get('violations', []))
                })
        
        if all_violations:
            print("VIOLATIONS REQUIRING ATTENTION:")
            print("-" * 30)
            for violation in all_violations:
                print(f"{violation['rule']}: {violation['manager']}")
                for issue in violation['issues']:
                    print(f"  - {issue}")
                print()
        else:
            print("NO CRITICAL VIOLATIONS FOUND")
            print()
        
        # Generate recommendations
        if self.audit_results['overall_compliance'] >= 95.0:
            print("AUDIT CONCLUSION: ARCHITECTURE COMPLIANCE EXCELLENT")
            print("Phase 3e Step 8.2 - COMPLETE")
        elif self.audit_results['overall_compliance'] >= 85.0:
            print("AUDIT CONCLUSION: ARCHITECTURE COMPLIANCE GOOD")
            print("Minor issues should be addressed for complete compliance")
        else:
            print("AUDIT CONCLUSION: ARCHITECTURE IMPROVEMENTS NEEDED")
            print("Significant violations require attention before Phase 3e completion")


def main():
    """Execute Phase 3e Step 8.2 Architecture Compliance Audit"""
    audit = Phase3eArchitectureAudit()
    results = audit.execute_full_audit()
    return results

if __name__ == "__main__":
    main()