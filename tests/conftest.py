"""
Ash-NLP Test Fixtures
---
FILE VERSION: v5.0-3-5.4-2
Repository: https://github.com/the-alphabet-cartel/ash-nlp
Community: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org

Shared pytest fixtures for the Ash-NLP test suite.
"""

import os
import sys
from pathlib import Path
from typing import Generator
from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient

# Ensure src is importable
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# Set test environment
os.environ["NLP_ENVIRONMENT"] = "testing"


# =============================================================================
# Configuration Fixtures
# =============================================================================


@pytest.fixture
def config_manager():
    """Create a ConfigManager for testing."""
    from src.managers import create_config_manager

    return create_config_manager(environment="testing")


@pytest.fixture
def test_config_dir(tmp_path) -> Path:
    """Create temporary config directory with test files."""
    config_dir = tmp_path / "config"
    config_dir.mkdir()

    # Create minimal default.json
    default_json = config_dir / "default.json"
    default_json.write_text("""{
        "api": {
            "host": "0.0.0.0",
            "port": 30880,
            "workers": 1
        },
        "models": {
            "device": "cpu",
            "warmup_enabled": false,
            "weights": {
                "bart": 0.50,
                "sentiment": 0.25,
                "irony": 0.15,
                "emotions": 0.10
            }
        },
        "thresholds": {
            "critical": 0.85,
            "high": 0.70,
            "medium": 0.50,
            "low": 0.30
        }
    }""")

    # Create testing.json
    testing_json = config_dir / "testing.json"
    testing_json.write_text("""{
        "models": {
            "device": "cpu",
            "warmup_enabled": false
        }
    }""")

    return config_dir


# =============================================================================
# Mock Model Fixtures
# =============================================================================


@pytest.fixture
def mock_model_result():
    """Create a mock ModelResult factory."""
    from src.models import ModelResult, ModelRole

    def _create_result(
        label: str = "test_label",
        score: float = 0.85,
        all_scores: dict = None,
        model_name: str = "test_model",
        role: ModelRole = ModelRole.PRIMARY,
        success: bool = True,
    ):
        return ModelResult(
            label=label,
            score=score,
            all_scores=all_scores or {label: score},
            latency_ms=50.0,
            model_name=model_name,
            model_role=role,
            success=success,
            error=None if success else "Test error",
        )

    return _create_result


@pytest.fixture
def mock_bart_result(mock_model_result):
    """Create mock BART result."""
    from src.models import ModelRole

    return mock_model_result(
        label="emotional distress",
        score=0.85,
        all_scores={
            "emotional distress": 0.85,
            "casual conversation": 0.10,
            "positive sharing": 0.05,
        },
        model_name="bart",
        role=ModelRole.PRIMARY,
    )


@pytest.fixture
def mock_sentiment_result(mock_model_result):
    """Create mock sentiment result."""
    from src.models import ModelRole

    return mock_model_result(
        label="negative",
        score=0.90,
        all_scores={
            "negative": 0.90,
            "neutral": 0.07,
            "positive": 0.03,
        },
        model_name="sentiment",
        role=ModelRole.SECONDARY,
    )


@pytest.fixture
def mock_irony_result(mock_model_result):
    """Create mock irony result (non-ironic)."""
    from src.models import ModelRole

    return mock_model_result(
        label="non_irony",
        score=0.95,
        all_scores={
            "non_irony": 0.95,
            "irony": 0.05,
        },
        model_name="irony",
        role=ModelRole.TERTIARY,
    )


@pytest.fixture
def mock_emotions_result(mock_model_result):
    """Create mock emotions result."""
    from src.models import ModelRole

    return mock_model_result(
        label="sadness",
        score=0.75,
        all_scores={
            "sadness": 0.75,
            "fear": 0.15,
            "neutral": 0.10,
        },
        model_name="emotions",
        role=ModelRole.SUPPLEMENTARY,
    )


# =============================================================================
# Mock Engine Fixture
# =============================================================================


@pytest.fixture
def mock_engine():
    """Create a mock DecisionEngine."""
    from src.ensemble import CrisisAssessment, CrisisSeverity

    engine = MagicMock()

    # Default assessment for testing
    engine.analyze.return_value = CrisisAssessment(
        crisis_detected=True,
        severity=CrisisSeverity.HIGH,
        confidence=0.85,
        crisis_score=0.78,
        requires_intervention=True,
        recommended_action="priority_response",
        signals={
            "bart": {
                "label": "emotional distress",
                "score": 0.85,
                "crisis_signal": 0.85,
            },
            "sentiment": {"label": "negative", "score": 0.90, "crisis_signal": 0.75},
        },
        processing_time_ms=125.5,
        models_used=["bart", "sentiment", "irony", "emotions"],
        is_degraded=False,
        degradation_reason="",
        message="Test message",
    )

    engine.is_ready.return_value = True
    engine.get_health.return_value = {
        "status": "healthy",
        "ready": True,
        "degraded": False,
        "models_loaded": 4,
        "total_models": 4,
    }
    engine.get_status.return_value = {
        "is_ready": True,
        "is_degraded": False,
        "degradation_reason": "",
        "async_inference": True,
        "stats": {
            "total_requests": 100,
            "crisis_detections": 15,
            "average_latency_ms": 125.0,
        },
        "models": {
            "models": {
                "bart": {"loaded": True, "enabled": True, "device": "cpu"},
                "sentiment": {"loaded": True, "enabled": True, "device": "cpu"},
                "irony": {"loaded": True, "enabled": True, "device": "cpu"},
                "emotions": {"loaded": True, "enabled": True, "device": "cpu"},
            }
        },
        "weights": {"bart": 0.50, "sentiment": 0.25, "irony": 0.15, "emotions": 0.10},
        "thresholds": {"critical": 0.85, "high": 0.70, "medium": 0.50, "low": 0.30},
    }

    return engine


# =============================================================================
# API Test Client Fixtures
# =============================================================================


@pytest.fixture
def app(mock_engine):
    """Create FastAPI app with mocked engine."""
    from src.api import create_app

    application = create_app(
        enable_cors=True,
        enable_rate_limiting=False,
    )

    # Inject mock engine
    application.state.engine = mock_engine
    application.state.config = None
    application.state.start_time = 0

    return application


@pytest.fixture
def client(app) -> Generator[TestClient, None, None]:
    """Create test client for API testing."""
    with TestClient(app, raise_server_exceptions=False) as test_client:
        yield test_client


@pytest.fixture
def client_no_engine():
    """Create test client without initialized engine."""
    from src.api import create_app

    application = create_app(
        enable_cors=True,
        enable_rate_limiting=False,
    )

    # No engine injected - simulates uninitialized state
    application.state.engine = None
    application.state.config = None
    application.state.start_time = 0

    with TestClient(application, raise_server_exceptions=False) as test_client:
        yield test_client


# =============================================================================
# Test Data Fixtures
# =============================================================================


@pytest.fixture
def crisis_messages():
    """Sample messages that should trigger crisis detection."""
    return [
        "I don't know if I can keep going anymore",
        "I just want the pain to stop",
        "Nobody would miss me if I was gone",
        "I'm having thoughts of hurting myself",
        "I feel so hopeless and alone",
    ]


@pytest.fixture
def safe_messages():
    """Sample messages that should NOT trigger crisis detection."""
    return [
        "I'm having a great day!",
        "Just finished lunch, it was delicious",
        "Looking forward to the weekend",
        "Has anyone played the new game?",
        "The weather is nice today",
    ]


@pytest.fixture
def edge_case_messages():
    """Edge case messages for testing."""
    return [
        "",  # Empty
        " ",  # Whitespace only
        "a" * 10000,  # Very long
        "🎮🎮🎮",  # Emoji only
        "I'm SO happy 🙄",  # Sarcastic (irony test)
        "kill it! this game is awesome!",  # Violence word, safe context
    ]
