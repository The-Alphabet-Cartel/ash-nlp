#!/usr/bin/env python3
"""
Ash-NLP: Crisis Detection Backend for The Alphabet Cartel Discord Community
CORE PRINCIPLE: Multi-Model Ensemble → Weighted Decision Engine → Crisis Classification
******************  CORE SYSTEM VISION (Never to be violated):  ****************
Ash-NLP is a CRISIS DETECTION BACKEND that:
1. PRIMARY: Uses BART Zero-Shot Classification for semantic crisis detection
2. CONTEXTUAL: Enhances with sentiment, irony, and emotion model signals
3. ENSEMBLE: Combines weighted model outputs through decision engine
4. PURPOSE: Detect crisis messages in Discord community communications
********************************************************************************
Installation Verification Script
---
FILE VERSION: v5.0-3-5.1-1
LAST MODIFIED: 2025-12-31
PHASE: Phase 3 - Pre-Deployment Verification
Repository: https://github.com/the-alphabet-cartel/ash-nlp
Community: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org

USAGE:
    python verify_installation.py

    # Or from Docker
    docker exec ash-nlp python verify_installation.py

This script verifies:
1. All Python dependencies are installed
2. All module imports work correctly
3. Configuration loads and validates
4. Model wrappers initialize properly
5. Ensemble components wire together
6. API application creates successfully
"""

import sys
import os
from pathlib import Path

# Ensure we're in the right directory
SCRIPT_DIR = Path(__file__).parent.absolute()
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

# =============================================================================
# Test Results Tracking
# =============================================================================


class TestResults:
    """Track verification test results."""

    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.warnings = 0
        self.errors = []

    def ok(self, message: str) -> None:
        """Record passed test."""
        self.passed += 1
        print(f"  ✅ {message}")

    def fail(self, message: str, error: str = None) -> None:
        """Record failed test."""
        self.failed += 1
        print(f"  ❌ {message}")
        if error:
            print(f"     Error: {error}")
            self.errors.append(f"{message}: {error}")

    def warn(self, message: str) -> None:
        """Record warning."""
        self.warnings += 1
        print(f"  ⚠️  {message}")

    def section(self, title: str) -> None:
        """Print section header."""
        print(f"\n{'=' * 60}")
        print(f"  {title}")
        print(f"{'=' * 60}")

    def summary(self) -> bool:
        """Print summary and return success status."""
        print(f"\n{'=' * 60}")
        print(f"  VERIFICATION SUMMARY")
        print(f"{'=' * 60}")
        print(f"  ✅ Passed:   {self.passed}")
        print(f"  ❌ Failed:   {self.failed}")
        print(f"  ⚠️  Warnings: {self.warnings}")
        print(f"{'=' * 60}")

        if self.failed == 0:
            print("\n🎉 All verification checks passed!")
            print("   The system is ready for deployment.\n")
            return True
        else:
            print(f"\n💥 {self.failed} check(s) failed!")
            print("   Please fix the errors before deploying.\n")
            if self.errors:
                print("   Errors:")
                for err in self.errors:
                    print(f"   - {err}")
            print()
            return False


results = TestResults()


# =============================================================================
# Step 1: Check Python Version
# =============================================================================


def check_python_version():
    """Verify Python version is compatible."""
    results.section("Python Version")

    version = sys.version_info
    version_str = f"{version.major}.{version.minor}.{version.micro}"

    if version.major == 3 and version.minor >= 10:
        results.ok(f"Python {version_str} (3.10+ required)")
    elif version.major == 3 and version.minor >= 9:
        results.warn(f"Python {version_str} (3.10+ recommended, 3.9 may work)")
    else:
        results.fail(f"Python {version_str}", "Python 3.10+ required")


# =============================================================================
# Step 2: Check Dependencies
# =============================================================================


def check_dependencies():
    """Verify required packages are installed."""
    results.section("Dependencies")

    dependencies = [
        ("fastapi", "FastAPI web framework"),
        ("uvicorn", "ASGI server"),
        ("pydantic", "Data validation"),
        ("transformers", "HuggingFace transformers"),
        ("torch", "PyTorch"),
    ]

    for package, description in dependencies:
        try:
            __import__(package)
            results.ok(f"{package} - {description}")
        except ImportError as e:
            results.fail(f"{package} - {description}", str(e))

    # Check CUDA availability (warning only)
    try:
        import torch

        if torch.cuda.is_available():
            device_name = torch.cuda.get_device_name(0)
            results.ok(f"CUDA available ({device_name})")
        else:
            results.warn("CUDA not available (will use CPU)")
    except Exception as e:
        results.warn(f"Could not check CUDA: {e}")


# =============================================================================
# Step 3: Check Configuration
# =============================================================================


def check_configuration():
    """Verify configuration system works."""
    results.section("Configuration")

    # Check config files exist
    config_dir = SCRIPT_DIR / "config"

    config_files = ["default.json", "production.json", "testing.json"]
    for filename in config_files:
        filepath = config_dir / filename
        if filepath.exists():
            results.ok(f"Config file: {filename}")
        else:
            results.fail(f"Config file: {filename}", "File not found")

    # Try to load ConfigManager
    try:
        from src.managers import create_config_manager

        results.ok("ConfigManager import")

        # Create config manager
        config = create_config_manager(environment="production")
        results.ok("ConfigManager instantiation")

        # Check key methods
        api_config = config.get_api_config()
        if api_config and "port" in api_config:
            results.ok(f"API config loads (port: {api_config.get('port')})")
        else:
            results.fail("API config loads", "Missing port configuration")

        weights = config.get_model_weights()
        if weights and len(weights) == 4:
            total = sum(weights.values())
            results.ok(f"Model weights load (total: {total:.2f})")
        else:
            results.fail(
                "Model weights load",
                f"Expected 4 weights, got {len(weights) if weights else 0}",
            )

        thresholds = config.get_thresholds()
        if thresholds and "critical" in thresholds:
            results.ok(f"Thresholds load (critical: {thresholds.get('critical')})")
        else:
            results.fail("Thresholds load", "Missing critical threshold")

    except Exception as e:
        results.fail("Configuration system", str(e))


# =============================================================================
# Step 4: Check Model Wrappers
# =============================================================================


def check_model_wrappers():
    """Verify model wrapper imports and initialization."""
    results.section("Model Wrappers")

    try:
        from src.models import (
            BaseModelWrapper,
            ModelResult,
            ModelRole,
            ModelTask,
        )

        results.ok("Base classes import")
    except Exception as e:
        results.fail("Base classes import", str(e))
        return

    # Check each model wrapper
    model_checks = [
        ("BARTCrisisClassifier", "create_bart_classifier", "BART (Primary)"),
        ("SentimentAnalyzer", "create_sentiment_analyzer", "Sentiment (Secondary)"),
        ("IronyDetector", "create_irony_detector", "Irony (Tertiary)"),
        (
            "EmotionsClassifier",
            "create_emotions_classifier",
            "Emotions (Supplementary)",
        ),
    ]

    for class_name, factory_name, description in model_checks:
        try:
            from src import models

            cls = getattr(models, class_name)
            factory = getattr(models, factory_name)

            # Create instance without loading model
            instance = factory()

            if instance.name and instance.weight > 0:
                results.ok(f"{description} wrapper (weight: {instance.weight})")
            else:
                results.fail(f"{description} wrapper", "Invalid configuration")

        except Exception as e:
            results.fail(f"{description} wrapper", str(e))


# =============================================================================
# Step 5: Check Ensemble Components
# =============================================================================


def check_ensemble():
    """Verify ensemble system components."""
    results.section("Ensemble System")

    # Model Loader
    try:
        from src.ensemble import ModelLoader, create_model_loader

        loader = create_model_loader(lazy_load=True, warmup_on_load=False)
        results.ok("ModelLoader")
    except Exception as e:
        results.fail("ModelLoader", str(e))

    # Weighted Scorer
    try:
        from src.ensemble import WeightedScorer, create_weighted_scorer, CrisisSeverity

        scorer = create_weighted_scorer()

        # Verify severity enum
        if CrisisSeverity.CRITICAL.value == "critical":
            results.ok("WeightedScorer")
        else:
            results.fail("WeightedScorer", "Invalid severity enum")
    except Exception as e:
        results.fail("WeightedScorer", str(e))

    # Fallback Strategy
    try:
        from src.ensemble import FallbackStrategy, create_fallback_strategy

        fallback = create_fallback_strategy()

        if fallback.is_operational():
            results.ok("FallbackStrategy")
        else:
            results.warn("FallbackStrategy created but not operational")
    except Exception as e:
        results.fail("FallbackStrategy", str(e))

    # Decision Engine
    try:
        from src.ensemble import EnsembleDecisionEngine, create_decision_engine

        # Create without auto-initialize (don't load models)
        engine = create_decision_engine(auto_initialize=False)
        results.ok("DecisionEngine")
    except Exception as e:
        results.fail("DecisionEngine", str(e))


# =============================================================================
# Step 6: Check API Components
# =============================================================================


def check_api():
    """Verify API components."""
    results.section("API Components")

    # Schemas
    try:
        from src.api import (
            AnalyzeRequest,
            AnalyzeResponse,
            HealthResponse,
            SeverityLevel,
        )

        # Test request validation
        request = AnalyzeRequest(message="Test message")
        if request.message == "Test message":
            results.ok("API schemas")
        else:
            results.fail("API schemas", "Validation not working")
    except Exception as e:
        results.fail("API schemas", str(e))

    # Middleware
    try:
        from src.api import (
            RequestIDMiddleware,
            LoggingMiddleware,
            setup_middleware,
        )

        results.ok("API middleware")
    except Exception as e:
        results.fail("API middleware", str(e))

    # Routes
    try:
        from src.api import (
            analysis_router,
            health_router,
            models_router,
        )

        results.ok("API routers")
    except Exception as e:
        results.fail("API routers", str(e))

    # Application Factory
    try:
        from src.api import create_app

        # Create app without starting it
        # Note: This won't initialize models (happens in lifespan)
        app = create_app(enable_rate_limiting=False)

        if app.title == "Ash-NLP":
            results.ok("FastAPI application")
        else:
            results.fail("FastAPI application", "Unexpected app title")
    except Exception as e:
        results.fail("FastAPI application", str(e))


# =============================================================================
# Step 7: Check File Structure
# =============================================================================


def check_file_structure():
    """Verify required files exist."""
    results.section("File Structure")

    required_files = [
        "main.py",
        "requirements.txt",
        "Dockerfile",
        "docker-compose.yml",
        "README.md",
        "src/__init__.py",
        "src/managers/__init__.py",
        "src/managers/config_manager.py",
        "src/managers/secrets_manager.py",
        "src/models/__init__.py",
        "src/models/base.py",
        "src/models/bart_classifier.py",
        "src/models/sentiment.py",
        "src/models/irony.py",
        "src/models/emotions.py",
        "src/ensemble/__init__.py",
        "src/ensemble/model_loader.py",
        "src/ensemble/scoring.py",
        "src/ensemble/fallback.py",
        "src/ensemble/decision_engine.py",
        "src/api/__init__.py",
        "src/api/app.py",
        "src/api/routes.py",
        "src/api/schemas.py",
        "src/api/middleware.py",
    ]

    missing = []
    for filepath in required_files:
        full_path = SCRIPT_DIR / filepath
        if not full_path.exists():
            missing.append(filepath)

    if not missing:
        results.ok(f"All {len(required_files)} required files present")
    else:
        for f in missing:
            results.fail(f"Missing: {f}")


# =============================================================================
# Step 8: Check Secrets
# =============================================================================


def check_secrets():
    """Verify secrets configuration."""
    results.section("Secrets")

    try:
        from src.managers import create_secrets_manager

        results.ok("SecretsManager import")

        secrets = create_secrets_manager()
        results.ok("SecretsManager instantiation")

        # Check secrets directory exists
        secrets_dir = SCRIPT_DIR / "secrets"
        if secrets_dir.exists():
            results.ok("Secrets directory exists")
        else:
            results.warn("Secrets directory missing (create ./secrets/)")

        # Check for HuggingFace token
        if secrets.has_secret("huggingface"):
            results.ok("HuggingFace token available")
        else:
            results.warn(
                "HuggingFace token not found "
                "(optional, but recommended for faster downloads)"
            )

        # Show secrets status
        status = secrets.get_status()
        docker_available = status.get("docker_secrets_available", False)
        local_available = status.get("local_secrets_available", False)

        if docker_available:
            results.ok("Docker secrets path available (/run/secrets/)")
        elif local_available:
            results.ok("Local secrets path available (./secrets/)")
        else:
            results.warn("No secrets paths available")

    except Exception as e:
        results.fail("Secrets system", str(e))


# =============================================================================
# Main
# =============================================================================


def main():
    """Run all verification checks."""
    print("\n" + "=" * 60)
    print("  Ash-NLP v5.0 Installation Verification")
    print("  Crisis Detection Backend")
    print("=" * 60)

    # Run all checks
    check_python_version()
    check_dependencies()
    check_file_structure()
    check_secrets()
    check_configuration()
    check_model_wrappers()
    check_ensemble()
    check_api()

    # Print summary and exit with appropriate code
    success = results.summary()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
