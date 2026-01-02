"""
Ash-NLP Configuration Tests
---
FILE VERSION: v5.0-3-5.4-3
Repository: https://github.com/the-alphabet-cartel/ash-nlp
Community: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org

Tests for the ConfigManager and configuration system.
"""

import os
import pytest
from pathlib import Path


class TestConfigManager:
    """Tests for ConfigManager class."""

    def test_create_config_manager(self):
        """Test factory function creates ConfigManager."""
        from src.managers import create_config_manager

        config = create_config_manager(environment="testing")
        assert config is not None
        assert config.environment == "testing"

    def test_default_environment(self):
        """Test default environment is production."""
        from src.managers import create_config_manager

        # Clear env var if set
        original = os.environ.pop("NLP_ENVIRONMENT", None)

        try:
            config = create_config_manager()
            # Should default to production or use env var
            assert config.environment in ("production", "testing")
        finally:
            if original:
                os.environ["NLP_ENVIRONMENT"] = original

    def test_get_api_config(self, config_manager):
        """Test API configuration retrieval."""
        api_config = config_manager.get_api_config()

        assert api_config is not None
        assert "port" in api_config
        assert "host" in api_config
        assert api_config["port"] == 30880

    def test_get_model_weights(self, config_manager):
        """Test model weights retrieval."""
        weights = config_manager.get_model_weights()

        assert weights is not None
        assert len(weights) == 4
        assert "bart" in weights
        assert "sentiment" in weights
        assert "irony" in weights
        assert "emotions" in weights

        # Check weights sum to approximately 1.0
        total = sum(weights.values())
        assert 0.99 <= total <= 1.01

    def test_get_thresholds(self, config_manager):
        """Test threshold retrieval."""
        thresholds = config_manager.get_thresholds()

        assert thresholds is not None
        assert "critical" in thresholds
        assert "high" in thresholds
        assert "medium" in thresholds
        assert "low" in thresholds

        # Check ordering
        assert thresholds["critical"] > thresholds["high"]
        assert thresholds["high"] > thresholds["medium"]
        assert thresholds["medium"] > thresholds["low"]

    def test_get_model_config(self, config_manager):
        """Test individual model config retrieval."""
        bart_config = config_manager.get_model_config("bart")

        assert bart_config is not None
        assert "weight" in bart_config or "enabled" in bart_config

    def test_get_performance_config(self, config_manager):
        """Test performance config retrieval."""
        perf_config = config_manager.get_performance_config()

        # May be None if not configured
        if perf_config is not None:
            assert isinstance(perf_config, dict)

    def test_environment_variable_override(self):
        """Test that environment variables override config."""
        from src.managers import create_config_manager

        # Set override
        os.environ["NLP_API_PORT"] = "9999"

        try:
            config = create_config_manager()
            api_config = config.get_api_config()

            # Should use env var value
            assert api_config["port"] == 9999
        finally:
            del os.environ["NLP_API_PORT"]


class TestConfigValidation:
    """Tests for configuration validation."""

    def test_weight_validation(self, config_manager):
        """Test that weights are valid (0-1 range)."""
        weights = config_manager.get_model_weights()

        for name, weight in weights.items():
            assert 0.0 <= weight <= 1.0, f"Weight for {name} out of range: {weight}"

    def test_threshold_validation(self, config_manager):
        """Test that thresholds are valid (0-1 range)."""
        thresholds = config_manager.get_thresholds()

        for name, threshold in thresholds.items():
            assert 0.0 <= threshold <= 1.0, (
                f"Threshold {name} out of range: {threshold}"
            )

    def test_port_validation(self, config_manager):
        """Test that port is valid."""
        api_config = config_manager.get_api_config()
        port = api_config.get("port", 30880)

        assert 1 <= port <= 65535


class TestConfigFiles:
    """Tests for configuration file existence."""

    @pytest.mark.skip(reason="Config files in src/config/, Docker maps to different location. FE-010")
    def test_default_config_exists(self):
        """Test default.json exists."""
        # Config files are in /app/config/, not /app/tests/config/
        config_path = Path("/app/config/default.json")
        assert config_path.exists(), "config/default.json not found"

    @pytest.mark.skip(reason="Config files in src/config/, Docker maps to different location. FE-010")
    def test_production_config_exists(self):
        """Test production.json exists (optional - may use default)."""
        config_path = Path("/app/config/production.json")
        # Production config is optional - system falls back to default
        # Just check the default exists if production doesn't
        default_path = Path("/app/config/default.json")
        assert config_path.exists() or default_path.exists(), \
            "Neither production.json nor default.json found in /app/config/"

    @pytest.mark.skip(reason="Config files in src/config/, Docker maps to different location. FE-010")
    def test_testing_config_exists(self):
        """Test testing.json exists (optional - may use default)."""
        config_path = Path("/app/config/testing.json")
        # Testing config is optional - system falls back to default
        default_path = Path("/app/config/default.json")
        assert config_path.exists() or default_path.exists(), \
            "Neither testing.json nor default.json found in /app/config/"
