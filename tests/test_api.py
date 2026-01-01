"""
Ash-NLP API Tests
---
FILE VERSION: v5.0-3-5.4-6
Repository: https://github.com/the-alphabet-cartel/ash-nlp
Community: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org

Tests for FastAPI endpoints using TestClient with mocked decision engine.
"""

import pytest


class TestRootEndpoint:
    """Tests for root endpoint."""

    def test_root_returns_service_info(self, client):
        """Test root endpoint returns service info."""
        response = client.get("/")

        assert response.status_code == 200
        data = response.json()

        assert data["service"] == "ash-nlp"
        assert "version" in data
        assert "docs" in data


class TestHealthEndpoints:
    """Tests for health check endpoints."""

    def test_health_endpoint(self, client):
        """Test /health returns healthy status."""
        response = client.get("/health")

        assert response.status_code == 200
        data = response.json()

        assert data["status"] == "healthy"
        assert data["ready"] is True
        assert "models_loaded" in data

    def test_healthz_endpoint(self, client):
        """Test /healthz (Kubernetes style) returns healthy."""
        response = client.get("/healthz")

        assert response.status_code == 200
        data = response.json()

        assert data["status"] == "healthy"

    def test_ready_endpoint(self, client):
        """Test /ready returns ready status."""
        response = client.get("/ready")

        assert response.status_code == 200
        data = response.json()

        assert data["ready"] is True

    def test_health_when_not_initialized(self, client_no_engine):
        """Test health returns unhealthy when engine not initialized."""
        response = client_no_engine.get("/health")

        # Should return 503 when not ready
        assert response.status_code == 503
        data = response.json()

        assert data["status"] == "unhealthy"
        assert data["ready"] is False


class TestStatusEndpoint:
    """Tests for status endpoint."""

    def test_status_endpoint(self, client):
        """Test /status returns detailed status."""
        response = client.get("/status")

        assert response.status_code == 200
        data = response.json()

        assert data["service"] == "ash-nlp"
        assert "version" in data
        assert "models" in data
        assert "stats" in data
        assert "config" in data

    def test_status_includes_weights(self, client):
        """Test status includes model weights."""
        response = client.get("/status")

        data = response.json()
        config = data.get("config", {})

        assert "weights" in config
        weights = config["weights"]

        assert weights["bart"] == 0.50
        assert weights["sentiment"] == 0.25


class TestAnalyzeEndpoint:
    """Tests for /analyze endpoint."""

    def test_analyze_valid_message(self, client):
        """Test analyzing a valid message."""
        response = client.post(
            "/analyze", json={"message": "I'm feeling overwhelmed today"}
        )

        assert response.status_code == 200
        data = response.json()

        assert "crisis_detected" in data
        assert "severity" in data
        assert "confidence" in data
        assert "crisis_score" in data
        assert "signals" in data
        assert "processing_time_ms" in data

    def test_analyze_with_metadata(self, client):
        """Test analyzing with optional metadata."""
        response = client.post(
            "/analyze",
            json={
                "message": "Test message",
                "user_id": "user_123",
                "channel_id": "general",
                "metadata": {"source": "test"},
            },
        )

        assert response.status_code == 200

    def test_analyze_empty_message(self, client):
        """Test analyzing empty message returns validation error."""
        response = client.post("/analyze", json={"message": ""})

        assert response.status_code == 422  # Validation error

    def test_analyze_whitespace_message(self, client):
        """Test analyzing whitespace-only message returns error."""
        response = client.post("/analyze", json={"message": "   "})

        assert response.status_code == 422

    def test_analyze_missing_message(self, client):
        """Test missing message field returns error."""
        response = client.post("/analyze", json={})

        assert response.status_code == 422

    def test_analyze_response_has_request_id(self, client):
        """Test response includes request ID."""
        response = client.post("/analyze", json={"message": "Test message"})

        assert response.status_code == 200

        # Check header
        assert "X-Request-ID" in response.headers

    def test_analyze_when_not_initialized(self, client_no_engine):
        """Test analyze returns 503 when engine not ready."""
        response = client_no_engine.post("/analyze", json={"message": "Test message"})

        assert response.status_code == 503


class TestBatchAnalyzeEndpoint:
    """Tests for /analyze/batch endpoint."""

    def test_batch_analyze_valid(self, client):
        """Test batch analyzing multiple messages."""
        response = client.post(
            "/analyze/batch",
            json={
                "messages": [
                    "I'm feeling great!",
                    "Everything is falling apart",
                    "Just had lunch",
                ]
            },
        )

        assert response.status_code == 200
        data = response.json()

        assert data["total_messages"] == 3
        assert "crisis_count" in data
        assert "results" in data
        assert len(data["results"]) == 3

    def test_batch_analyze_empty_list(self, client):
        """Test batch with empty list returns error."""
        response = client.post("/analyze/batch", json={"messages": []})

        assert response.status_code == 422

    def test_batch_analyze_single_message(self, client):
        """Test batch with single message works."""
        response = client.post("/analyze/batch", json={"messages": ["Single message"]})

        assert response.status_code == 200
        data = response.json()

        assert data["total_messages"] == 1


class TestModelsEndpoint:
    """Tests for /models endpoints."""

    def test_list_models(self, client):
        """Test listing all models."""
        response = client.get("/models")

        assert response.status_code == 200
        data = response.json()

        assert isinstance(data, list)
        assert len(data) == 4  # bart, sentiment, irony, emotions

    def test_get_model_details(self, client):
        """Test getting specific model details."""
        response = client.get("/models/bart")

        assert response.status_code == 200
        data = response.json()

        assert data["name"] == "bart"
        assert "loaded" in data
        assert "weight" in data

    def test_get_invalid_model(self, client):
        """Test getting non-existent model returns 404."""
        response = client.get("/models/invalid_model")

        assert response.status_code == 404


class TestMiddleware:
    """Tests for middleware functionality."""

    def test_request_id_generated(self, client):
        """Test request ID is generated and returned."""
        response = client.get("/health")

        assert "X-Request-ID" in response.headers
        request_id = response.headers["X-Request-ID"]

        assert request_id.startswith("req_")

    def test_custom_request_id_accepted(self, client):
        """Test custom request ID is accepted."""
        custom_id = "custom_test_123"

        response = client.get("/health", headers={"X-Request-ID": custom_id})

        assert response.headers["X-Request-ID"] == custom_id

    def test_invalid_request_id_replaced(self, client):
        """Test invalid request ID is replaced with generated one."""
        # Too long request ID should be replaced
        invalid_id = "x" * 100

        response = client.get("/health", headers={"X-Request-ID": invalid_id})

        # Should have a valid generated ID instead
        assert response.headers["X-Request-ID"] != invalid_id
        assert response.headers["X-Request-ID"].startswith("req_")


class TestErrorHandling:
    """Tests for error handling."""

    def test_invalid_json_returns_422(self, client):
        """Test invalid JSON returns validation error."""
        response = client.post(
            "/analyze",
            content="not valid json",
            headers={"Content-Type": "application/json"},
        )

        assert response.status_code == 422

    def test_wrong_content_type(self, client):
        """Test wrong content type returns error."""
        response = client.post(
            "/analyze",
            content="message=test",
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )

        assert response.status_code == 422


class TestAPIDocumentation:
    """Tests for API documentation endpoints."""

    def test_openapi_available(self, client):
        """Test OpenAPI schema is available."""
        response = client.get("/openapi.json")

        assert response.status_code == 200
        data = response.json()

        assert "openapi" in data
        assert "info" in data
        assert data["info"]["title"] == "Ash-NLP"

    def test_docs_endpoint(self, client):
        """Test Swagger UI docs endpoint."""
        response = client.get("/docs")

        # Should redirect or return HTML
        assert response.status_code == 200

    def test_redoc_endpoint(self, client):
        """Test ReDoc docs endpoint."""
        response = client.get("/redoc")

        assert response.status_code == 200


class TestSchemas:
    """Tests for Pydantic schema validation."""

    def test_analyze_request_validation(self):
        """Test AnalyzeRequest validation."""
        from src.api import AnalyzeRequest

        # Valid request
        request = AnalyzeRequest(message="Test message")
        assert request.message == "Test message"

        # Message is trimmed
        request = AnalyzeRequest(message="  padded  ")
        assert request.message == "padded"

    def test_analyze_request_length_validation(self):
        """Test message length validation."""
        from src.api import AnalyzeRequest
        from pydantic import ValidationError

        # Too long message should fail
        with pytest.raises(ValidationError):
            AnalyzeRequest(message="x" * 10001)

    def test_severity_level_enum(self):
        """Test SeverityLevel enum."""
        from src.api import SeverityLevel

        assert SeverityLevel.CRITICAL.value == "critical"
        assert SeverityLevel.SAFE.value == "safe"

    def test_health_response_schema(self):
        """Test HealthResponse schema."""
        from src.api import HealthResponse, HealthStatus
        from datetime import datetime

        response = HealthResponse(
            status=HealthStatus.HEALTHY,
            ready=True,
            degraded=False,
            models_loaded=4,
            total_models=4,
            version="v5.0",
        )

        assert response.status == HealthStatus.HEALTHY
        assert response.ready is True
