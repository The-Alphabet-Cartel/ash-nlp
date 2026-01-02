"""
Ash-NLP Model Wrapper Tests
---
FILE VERSION: v5.0-3-5.4-4
Repository: https://github.com/the-alphabet-cartel/ash-nlp
Community: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org

Tests for model wrappers. These tests verify initialization and interface
without loading actual HuggingFace models (to keep tests fast).
"""

import pytest


class TestModelResult:
    """Tests for ModelResult dataclass."""

    def test_model_result_creation(self, mock_model_result):
        """Test ModelResult can be created."""
        result = mock_model_result()

        assert result.label == "test_label"
        assert result.score == 0.85
        assert result.success is True
        assert result.error is None

    def test_model_result_failure(self, mock_model_result):
        """Test ModelResult with failure state."""
        result = mock_model_result(success=False)

        assert result.success is False
        assert result.error is not None

    def test_model_result_to_dict(self, mock_model_result):
        """Test ModelResult conversion to dict."""
        result = mock_model_result()

        result_dict = result.to_dict()

        assert isinstance(result_dict, dict)
        assert "label" in result_dict
        assert "score" in result_dict
        assert "success" in result_dict


class TestModelRole:
    """Tests for ModelRole enum."""

    def test_model_roles_exist(self):
        """Test all expected roles exist."""
        from src.models import ModelRole

        assert hasattr(ModelRole, "PRIMARY")
        assert hasattr(ModelRole, "SECONDARY")
        assert hasattr(ModelRole, "TERTIARY")
        assert hasattr(ModelRole, "SUPPLEMENTARY")

    def test_model_role_values(self):
        """Test role values are strings."""
        from src.models import ModelRole

        assert ModelRole.PRIMARY.value == "primary"
        assert ModelRole.SECONDARY.value == "secondary"


class TestBARTClassifier:
    """Tests for BARTCrisisClassifier wrapper."""

    def test_bart_import(self):
        """Test BART classifier can be imported."""
        from src.models import BARTCrisisClassifier, create_bart_classifier

        assert BARTCrisisClassifier is not None
        assert create_bart_classifier is not None

    def test_bart_factory(self, config_manager):
        """Test BART factory function."""
        from src.models import create_bart_classifier

        bart = create_bart_classifier(config_manager=config_manager)

        assert bart is not None
        # Model name is bart_crisis (updated in v5.0)
        assert bart.name in ["bart", "bart_crisis"]
        assert bart.weight == 0.50

    def test_bart_default_labels(self):
        """Test BART has default crisis labels."""
        from src.models import create_bart_classifier

        bart = create_bart_classifier()
        labels = bart.get_crisis_labels()

        assert len(labels) > 0
        assert "suicide ideation" in labels or "emotional distress" in labels

    def test_bart_is_primary(self):
        """Test BART has PRIMARY role."""
        from src.models import create_bart_classifier, ModelRole

        bart = create_bart_classifier()

        assert bart.role == ModelRole.PRIMARY


class TestSentimentAnalyzer:
    """Tests for SentimentAnalyzer wrapper."""

    def test_sentiment_import(self):
        """Test sentiment analyzer can be imported."""
        from src.models import SentimentAnalyzer, create_sentiment_analyzer

        assert SentimentAnalyzer is not None
        assert create_sentiment_analyzer is not None

    def test_sentiment_factory(self, config_manager):
        """Test sentiment factory function."""
        from src.models import create_sentiment_analyzer

        sentiment = create_sentiment_analyzer(config_manager=config_manager)

        assert sentiment is not None
        assert sentiment.name == "sentiment"
        assert sentiment.weight == 0.25

    def test_sentiment_is_secondary(self):
        """Test sentiment has SECONDARY role."""
        from src.models import create_sentiment_analyzer, ModelRole

        sentiment = create_sentiment_analyzer()

        assert sentiment.role == ModelRole.SECONDARY


class TestIronyDetector:
    """Tests for IronyDetector wrapper."""

    def test_irony_import(self):
        """Test irony detector can be imported."""
        from src.models import IronyDetector, create_irony_detector

        assert IronyDetector is not None
        assert create_irony_detector is not None

    def test_irony_factory(self, config_manager):
        """Test irony factory function."""
        from src.models import create_irony_detector

        irony = create_irony_detector(config_manager=config_manager)

        assert irony is not None
        assert irony.name == "irony"
        assert irony.weight == 0.15

    def test_irony_is_tertiary(self):
        """Test irony has TERTIARY role."""
        from src.models import create_irony_detector, ModelRole

        irony = create_irony_detector()

        assert irony.role == ModelRole.TERTIARY


class TestEmotionsClassifier:
    """Tests for EmotionsClassifier wrapper."""

    def test_emotions_import(self):
        """Test emotions classifier can be imported."""
        from src.models import EmotionsClassifier, create_emotions_classifier

        assert EmotionsClassifier is not None
        assert create_emotions_classifier is not None

    def test_emotions_factory(self, config_manager):
        """Test emotions factory function."""
        from src.models import create_emotions_classifier

        emotions = create_emotions_classifier(config_manager=config_manager)

        assert emotions is not None
        assert emotions.name == "emotions"
        assert emotions.weight == 0.10

    def test_emotions_is_supplementary(self):
        """Test emotions has SUPPLEMENTARY role."""
        from src.models import create_emotions_classifier, ModelRole

        emotions = create_emotions_classifier()

        assert emotions.role == ModelRole.SUPPLEMENTARY


class TestModelPackage:
    """Tests for models package exports."""

    def test_all_exports(self):
        """Test all expected exports are available."""
        from src.models import (
            BaseModelWrapper,
            ModelResult,
            ModelRole,
            ModelTask,
            ModelInfo,
            BARTCrisisClassifier,
            SentimentAnalyzer,
            IronyDetector,
            EmotionsClassifier,
            create_bart_classifier,
            create_sentiment_analyzer,
            create_irony_detector,
            create_emotions_classifier,
        )

        # All imports should succeed
        assert BaseModelWrapper is not None
        assert ModelResult is not None

    def test_create_model_function(self):
        """Test generic model creation function."""
        from src.models import create_model

        # BART can be created with either alias
        bart = create_model("bart")
        assert bart is not None
        assert bart.name in ["bart", "bart_crisis"]

        sentiment = create_model("sentiment")
        assert sentiment is not None
        assert sentiment.name == "sentiment"

    def test_create_model_invalid(self):
        """Test create_model with invalid name raises ValueError."""
        from src.models import create_model

        with pytest.raises(ValueError) as exc_info:
            create_model("invalid_model")
        
        assert "invalid_model" in str(exc_info.value).lower() or "unknown" in str(exc_info.value).lower()
