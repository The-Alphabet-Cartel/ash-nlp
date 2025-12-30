#!/bin/bash
# Ash-NLP Testing Suite - Docker Entrypoint
# FILE VERSION: v5.0
# LAST MODIFIED: 2025-12-30
# CLEAN ARCHITECTURE: v5.0 Compliant
# Repository: https://github.com/the-alphabet-cartel/ash-nlp

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Banner
echo -e "${BLUE}"
echo "╔═══════════════════════════════════════════════════════════╗"
echo "║        Ash-NLP v5.0 Testing Suite Container              ║"
echo "║        The Alphabet Cartel - Crisis Detection            ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Check GPU availability
echo -e "${YELLOW}Checking GPU availability...${NC}"
if python -c "import torch; assert torch.cuda.is_available(), 'CUDA not available'" 2>/dev/null; then
    GPU_NAME=$(python -c "import torch; print(torch.cuda.get_device_name(0))")
    echo -e "${GREEN}✓ GPU detected: ${GPU_NAME}${NC}"
else
    echo -e "${YELLOW}⚠ No GPU detected - running in CPU mode${NC}"
    export TEST_DEVICE=cpu
fi

# Check transformers library
echo -e "${YELLOW}Checking dependencies...${NC}"
if python -c "import transformers" 2>/dev/null; then
    TRANSFORMERS_VERSION=$(python -c "import transformers; print(transformers.__version__)")
    echo -e "${GREEN}✓ Transformers ${TRANSFORMERS_VERSION} installed${NC}"
else
    echo -e "${RED}✗ Transformers not installed${NC}"
    exit 1
fi

# Display configuration
echo -e "${BLUE}Configuration:${NC}"
echo "  Device: ${TEST_DEVICE:-cuda}"
echo "  Batch Size: ${TEST_BATCH_SIZE:-8}"
echo "  Timeout: ${TEST_TIMEOUT:-30}s"
echo "  Verbose: ${TEST_VERBOSE:-true}"
echo ""

# Function to display help
show_help() {
    echo -e "${GREEN}Ash-NLP Testing Suite - Usage:${NC}"
    echo ""
    echo "Available commands:"
    echo ""
    echo -e "${YELLOW}Testing Commands:${NC}"
    echo "  test-model <model_name> <dataset>   - Test a single model"
    echo "  test-baseline                        - Test v3.1 baseline models"
    echo "  test-proposed                        - Test v5.0 proposed models"
    echo "  test-all                             - Run comprehensive test suite"
    echo "  compare <model_a> <model_b>          - Compare two models"
    echo ""
    echo -e "${YELLOW}Utility Commands:${NC}"
    echo "  bash                                 - Interactive bash shell"
    echo "  python                               - Interactive Python shell"
    echo "  ipython                              - IPython shell (if installed)"
    echo "  --help                               - Show this help message"
    echo ""
    echo -e "${YELLOW}Examples:${NC}"
    echo "  # Test BART model on crisis examples"
    echo "  docker-compose run ash-nlp-testing test-model facebook/bart-large-mnli crisis"
    echo ""
    echo "  # Run baseline comparison"
    echo "  docker-compose run ash-nlp-testing test-baseline"
    echo ""
    echo "  # Interactive shell"
    echo "  docker-compose run ash-nlp-testing bash"
    echo ""
    echo -e "${YELLOW}Docker Compose Examples:${NC}"
    echo "  # Start container in background"
    echo "  docker-compose -f docker-compose.testing.yml up -d"
    echo ""
    echo "  # Run tests"
    echo "  docker-compose -f docker-compose.testing.yml exec ash-nlp-testing test-all"
    echo ""
    echo "  # View logs"
    echo "  docker-compose -f docker-compose.testing.yml logs -f"
    echo ""
}

# Command routing
case "$1" in
    test-model)
        if [ -z "$2" ] || [ -z "$3" ]; then
            echo -e "${RED}Error: test-model requires <model_name> and <dataset>${NC}"
            echo "Usage: test-model facebook/bart-large-mnli crisis"
            exit 1
        fi

        MODEL_NAME="$2"
        DATASET="$3"

        echo -e "${GREEN}Testing model: ${MODEL_NAME}${NC}"
        echo -e "${GREEN}Dataset: ${DATASET}_examples.json${NC}"

        python <<EOF
from testing import create_model_evaluator

evaluator = create_model_evaluator()
results = evaluator.test_dataset(
    model_name="${MODEL_NAME}",
    dataset_path="testing/test_datasets/${DATASET}_examples.json",
    task_type="zero-shot-classification"
)

print("\n" + "="*60)
print("TEST RESULTS")
print("="*60)
print(f"Model: ${MODEL_NAME}")
print(f"Accuracy: {results['metrics']['overall']['accuracy']:.2%}")
print(f"Passed: {results['metrics']['overall']['passed']}/{results['metrics']['overall']['total_tests']}")
print(f"Avg Latency: {results['metrics']['performance']['avg_latency_ms']:.2f}ms")
print(f"Avg VRAM: {results['metrics']['performance']['avg_vram_mb']:.2f}MB")

# Save report
report = evaluator.generate_report(results, "testing/reports/output/test_results.json")
print("\nReport saved to: testing/reports/output/test_results.json")
EOF
        ;;

    test-baseline)
        echo -e "${GREEN}Testing v3.1 baseline models...${NC}"
        python <<EOF
from testing import create_model_evaluator

evaluator = create_model_evaluator()

# Test baseline model
print("\nTesting baseline: MoritzLaurer/deberta-v3-base-zeroshot-v2.0")
results = evaluator.test_dataset(
    model_name="MoritzLaurer/deberta-v3-base-zeroshot-v2.0",
    dataset_path="testing/test_datasets/crisis_examples.json",
    task_type="zero-shot-classification"
)

print(f"\nBaseline Accuracy: {results['metrics']['overall']['accuracy']:.2%}")
evaluator.generate_report(results, "testing/reports/output/baseline_v3.1.json")
print("Baseline report saved!")
EOF
        ;;

    test-proposed)
        echo -e "${GREEN}Testing v5.0 proposed models...${NC}"
        python <<EOF
from testing import create_model_evaluator

evaluator = create_model_evaluator()

models = [
    "facebook/bart-large-mnli",
    "SamLowe/roberta-base-go_emotions",
    "cardiffnlp/twitter-roberta-base-sentiment-latest",
    "cardiffnlp/twitter-roberta-base-irony"
]

for model in models:
    print(f"\n{'='*60}")
    print(f"Testing: {model}")
    print('='*60)

    results = evaluator.test_dataset(
        model_name=model,
        dataset_path="testing/test_datasets/crisis_examples.json",
        task_type="zero-shot-classification" if "bart" in model else "text-classification"
    )

    print(f"Accuracy: {results['metrics']['overall']['accuracy']:.2%}")
    print(f"Latency: {results['metrics']['performance']['avg_latency_ms']:.2f}ms")

    # Save individual report
    safe_name = model.replace("/", "_")
    evaluator.generate_report(results, f"testing/reports/output/{safe_name}_test.json")

print("\nAll proposed models tested!")
EOF
        ;;

    test-all)
        echo -e "${GREEN}Running comprehensive test suite...${NC}"
        python <<EOF
from testing import create_model_evaluator

evaluator = create_model_evaluator()

datasets = [
    "crisis_examples",
    "safe_examples",
    "edge_cases",
    "lgbtqia_specific"
]

print("\nTesting model: facebook/bart-large-mnli")
print("Against all datasets...\n")

all_results = {}
for dataset in datasets:
    print(f"Testing dataset: {dataset}")
    results = evaluator.test_dataset(
        model_name="facebook/bart-large-mnli",
        dataset_path=f"testing/test_datasets/{dataset}.json",
        task_type="zero-shot-classification"
    )
    all_results[dataset] = results
    print(f"  Accuracy: {results['metrics']['overall']['accuracy']:.2%}")

# Generate comprehensive report
evaluator.generate_report(all_results, "testing/reports/output/comprehensive_test.json")
print("\nComprehensive test complete!")
EOF
        ;;

    compare)
        if [ -z "$2" ] || [ -z "$3" ]; then
            echo -e "${RED}Error: compare requires <model_a> and <model_b>${NC}"
            exit 1
        fi

        echo -e "${GREEN}Comparing models...${NC}"
        python <<EOF
from testing import create_model_evaluator

evaluator = create_model_evaluator()
comparison = evaluator.compare_models(
    model_a="$2",
    model_b="$3",
    dataset_path="testing/test_datasets/crisis_examples.json",
    task_type="zero-shot-classification"
)

print("\n" + "="*60)
print("MODEL COMPARISON")
print("="*60)
print(f"Model A: $2")
print(f"Model B: $3")
print(f"\nAccuracy Improvement: {comparison['improvements']['accuracy']['percentage']:.2f}%")
print(f"Latency Change: {comparison['improvements']['latency']['percentage']:.2f}%")
print(f"\nWinner: {comparison['winner']}")

evaluator.generate_report(comparison, "testing/reports/output/model_comparison.json")
EOF
        ;;

    bash)
        echo -e "${GREEN}Starting interactive bash shell...${NC}"
        exec /bin/bash
        ;;

    python)
        echo -e "${GREEN}Starting Python shell...${NC}"
        exec python
        ;;

    ipython)
        echo -e "${GREEN}Starting IPython shell...${NC}"
        exec ipython
        ;;

    --help|-h|help)
        show_help
        ;;

    *)
        if [ -z "$1" ]; then
            show_help
        else
            echo -e "${YELLOW}Executing custom command: $@${NC}"
            exec "$@"
        fi
        ;;
esac
