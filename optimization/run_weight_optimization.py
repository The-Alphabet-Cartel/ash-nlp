#!/usr/bin/env python3
# ash-nlp/optimization/run_weight_optimization.py
"""
Ash-NLP: Crisis Detection Backend for The Alphabet Cartel Discord Community
CORE PRINCIPLE: Zero-Shot AI Models → Pattern Enhancement → Crisis Classification
******************  CORE SYSTEM VISION (Never to be violated):  ****************
Ash-NLP is a CRISIS DETECTION BACKEND that:
1. FIRST: Uses Zero-Shot AI models for primary semantic classification
2. SECOND: Enhances AI results with contextual pattern analysis  
3. FALLBACK: Uses pattern-only classification if AI models fail
4. PURPOSE: Detect crisis messages in Discord community communications
********************************************************************************
Weight Optimization Runner Script
---
FILE VERSION: v3.1-wo-1-1
LAST MODIFIED: 2025-09-01
PHASE: Weight Optimization Implementation
CLEAN ARCHITECTURE: v3.1 Compliant
Repository: https://github.com/the-alphabet-cartel/ash-nlp
Community: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org
"""

import sys
import logging
import argparse
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from optimization.weight_optimizer import create_weight_optimizer, OptimizationConfiguration
from optimization.test_data_loader import create_test_data_loader

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('optimization.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

def main():
    """Main optimization execution"""
    parser = argparse.ArgumentParser(description='Ash-NLP Ensemble Weight Optimization')
    parser.add_argument('--test-data-dir', default='./test_data', 
                       help='Directory containing test data JSON files')
    parser.add_argument('--generations', type=int, default=50,
                       help='Number of evolutionary algorithm generations')
    parser.add_argument('--population-size', type=int, default=20,
                       help='Population size for evolutionary algorithm')
    parser.add_argument('--sample-run', action='store_true',
                       help='Run with sample data for testing')
    parser.add_argument('--api-endpoint', default='http://localhost:8881/analyze',
                       help='NLP API endpoint for evaluation')
    
    args = parser.parse_args()
    
    logger.info("🚀 Starting Ash-NLP Weight Optimization")
    logger.info(f"Configuration: {args.generations} generations, {args.population_size} population")
    
    try:
        # Load test data
        logger.info("📊 Loading test dataset...")
        data_loader = create_test_data_loader(args.test_data_dir)
        
        if args.sample_run:
            logger.info("🧪 Running in sample mode with reduced dataset")
            test_dataset = data_loader.create_sample_dataset(sample_size=10)
        else:
            test_dataset = data_loader.load_all_test_data()
        
        # Validate dataset
        validation_report = data_loader.validate_dataset(test_dataset)
        if not validation_report['valid']:
            logger.error(f"Dataset validation failed: {validation_report['issues']}")
            return 1
        
        logger.info(f"✅ Dataset loaded: {validation_report['total_phrases']} total phrases")
        
        # Configure optimization
        config = OptimizationConfiguration(
            population_size=args.population_size,
            generations=args.generations,
            api_endpoint=args.api_endpoint
        )
        
        if args.sample_run:
            # Reduce parameters for sample run
            config.generations = 10
            config.population_size = 8
            logger.info("🧪 Sample run configuration applied")
        
        # Create optimizer
        optimizer = create_weight_optimizer(test_dataset, config)
        
        # Establish baseline
        logger.info("📏 Establishing baseline performance...")
        baseline_performance = optimizer.establish_baseline_performance()
        
        # Run optimization
        logger.info("🎯 Starting optimization process...")
        best_individual, optimization_results = optimizer.optimize_weights()
        
        # Save results
        logger.info("💾 Saving optimization results...")
        results_file = optimizer.save_results(optimization_results)
        
        # Print summary
        print("\n" + "="*80)
        print("🎉 OPTIMIZATION COMPLETE")
        print("="*80)
        
        summary = optimization_results['optimization_summary']
        print(f"📊 Improvement: {summary['improvement_percentage']:.2f}%")
        print(f"🎯 Target Met: {'YES' if summary['target_met'] else 'NO'}")
        print(f"⏱️  Total Time: {summary['total_time_minutes']:.1f} minutes")
        print(f"🔧 API Calls: {summary['total_api_calls']:,}")
        
        best_config = optimization_results['best_configuration']
        print(f"\n🏆 OPTIMAL CONFIGURATION:")
        print(f"   Ensemble Mode: {best_config['ensemble_mode']}")
        print(f"   Depression Weight: {best_config['weights']['depression']:.3f}")
        print(f"   Sentiment Weight: {best_config['weights']['sentiment']:.3f}")
        print(f"   Distress Weight: {best_config['weights']['emotional_distress']:.3f}")
        
        print(f"\n💡 Recommendation: {optimization_results['recommendation']}")
        print(f"📁 Results saved to: {results_file}")
        
        return 0 if summary['target_met'] else 2
        
    except KeyboardInterrupt:
        logger.info("⏹️  Optimization interrupted by user")
        return 130
    except Exception as e:
        logger.error(f"❌ Optimization failed: {e}")
        logger.exception("Full error details:")
        return 1

if __name__ == "__main__":
    sys.exit(main())