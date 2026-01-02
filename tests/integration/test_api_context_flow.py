"""
Ash-NLP Integration Tests: API Context Flow
---
FILE VERSION: v5.0-5-TEST-1.0
LAST MODIFIED: 2026-01-02
Repository: https://github.com/the-alphabet-cartel/ash-nlp
Community: The Alphabet Cartel - https://discord.gg/alphabetcartel | https://alphabetcartel.org

Integration tests for:
- Full API request/response flow with context analysis
- Message history in API requests
- Context analysis in API responses
- Escalation detection through API
- Context configuration endpoints
"""

import pytest
from datetime import datetime, timedelta
from typing import List, Dict, Any
from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient

from src.api import create_app
from src.ensemble import CrisisAssessment, CrisisSeverity


# =============================================================================
# Test Fixtures
# =============================================================================


@pytest.fixture
def mock_engine_with_context():
    """Create a mock DecisionEngine with context analysis support."""
    engine = MagicMock()
    
    def mock_analyze(message: str, **kwargs):
        """Mock analyze that includes context analysis."""
        message_history = kwargs.get("message_history", [])
        
        # Determine if this looks like escalation based on history
        is_escalation = len(message_history) >= 3
        is_crisis = "can't" in message.lower() or "help" in message.lower()
        
        return CrisisAssessment(
            crisis_detected=is_crisis,
            severity=CrisisSeverity.HIGH if is_crisis else CrisisSeverity.LOW,
            confidence=0.85 if is_crisis else 0.3,
            crisis_score=0.85 if is_crisis else 0.25,
            requires_intervention=is_crisis,
            recommended_action="priority_response" if is_crisis else "none",
            signals={
                "bart": {
                    "label": "emotional distress" if is_crisis else "casual",
                    "score": 0.85 if is_crisis else 0.2,
                    "crisis_signal": 0.85 if is_crisis else 0.2,
                }
            },
            processing_time_ms=125.5,
            models_used=["bart", "sentiment", "irony", "emotions"],
            is_degraded=False,
            degradation_reason="",
            message=message,
            # Phase 5 context analysis
            context_analysis={
                "escalation": {
                    "detected": is_escalation and is_crisis,
                    "rate": "rapid" if is_escalation and is_crisis else "none",
                    "confidence": 0.75 if is_escalation else 0.0,
                    "pattern_name": "evening_deterioration" if is_escalation else None,
                },
                "trend": {
                    "direction": "worsening" if is_escalation else "stable",
                    "velocity": "moderate" if is_escalation else "none",
                },
                "temporal": {
                    "late_night_risk": False,
                    "rapid_posting": False,
                    "is_weekend": False,
                    "time_risk_modifier": 1.0,
                },
                "intervention": {
                    "urgency": "high" if is_crisis and is_escalation else "none",
                    "recommended_point": 2 if is_escalation else None,
                },
                "trajectory": {
                    "scores": [0.3, 0.5, 0.7] if is_escalation else [],
                    "start_score": 0.3 if is_escalation else 0.0,
                    "end_score": 0.85 if is_escalation else 0.0,
                    "peak_score": 0.85 if is_escalation else 0.0,
                },
                "history_metadata": {
                    "message_count": len(message_history) + 1,
                    "time_span_hours": 4.0 if message_history else 0.0,
                },
            }
        )
    
    engine.analyze.side_effect = mock_analyze
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
        "models_used": ["bart", "sentiment", "irony", "emotions"],
    }
    
    return engine


@pytest.fixture
def app_with_context(mock_engine_with_context):
    """Create FastAPI app with context-aware mock engine."""
    application = create_app(
        enable_cors=True,
        enable_rate_limiting=False,
    )
    
    application.state.engine = mock_engine_with_context
    application.state.config = None
    application.state.start_time = 0
    
    return application


@pytest.fixture
def client_with_context(app_with_context):
    """Create test client with context support."""
    with TestClient(app_with_context, raise_server_exceptions=False) as test_client:
        yield test_client


@pytest.fixture
def base_timestamp():
    """Base timestamp for test data."""
    return datetime(2026, 1, 1, 14, 0, 0)


# =============================================================================
# Message History Generators
# =============================================================================


def create_api_message_history(
    base: datetime,
    count: int = 4,
    escalating: bool = True,
) -> List[Dict[str, Any]]:
    """Create message history in API request format."""
    messages = [
        "Just feeling a bit off today",
        "Things are getting harder",
        "I'm struggling more than usual",
        "I don't know if I can keep going",
    ]
    
    history = []
    for i in range(count):
        if escalating:
            score = 0.2 + (0.5 / (count - 1)) * i if count > 1 else 0.2
        else:
            score = 0.3
        
        history.append({
            "message": messages[i % len(messages)],
            "timestamp": (base + timedelta(hours=i)).isoformat() + "Z",
            "crisis_score": score,
            "message_id": f"msg_{i:03d}",
        })
    
    return history


# =============================================================================
# Test Cases: API Request with Message History
# =============================================================================


class TestAnalyzeWithMessageHistory:
    """Tests for /analyze endpoint with message history."""
    
    def test_analyze_without_history(self, client_with_context):
        """Test basic analysis without message history."""
        response = client_with_context.post(
            "/analyze",
            json={
                "message": "Hello, how are you?",
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "crisis_detected" in data
        assert "crisis_score" in data
    
    def test_analyze_with_history(self, client_with_context, base_timestamp):
        """Test analysis with message history."""
        history = create_api_message_history(base_timestamp, count=4)
        
        response = client_with_context.post(
            "/analyze",
            json={
                "message": "I can't take this anymore",
                "message_history": history,
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        
        # Should have context analysis in response
        assert "context_analysis" in data
        assert "escalation" in data["context_analysis"]
        assert "trend" in data["context_analysis"]
        assert "temporal" in data["context_analysis"]
    
    def test_analyze_detects_escalation(self, client_with_context, base_timestamp):
        """Test escalation is detected with escalating history."""
        history = create_api_message_history(
            base_timestamp, 
            count=4, 
            escalating=True
        )
        
        response = client_with_context.post(
            "/analyze",
            json={
                "message": "I need help now",
                "message_history": history,
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        
        # Check escalation detection
        context = data["context_analysis"]
        assert context["escalation"]["detected"] is True
        assert context["escalation"]["rate"] in ["rapid", "gradual", "sudden"]
    
    def test_analyze_stable_no_escalation(self, client_with_context, base_timestamp):
        """Test no escalation with stable history."""
        history = create_api_message_history(
            base_timestamp, 
            count=4, 
            escalating=False
        )
        
        response = client_with_context.post(
            "/analyze",
            json={
                "message": "Just checking in",
                "message_history": history,
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        
        # Check no escalation
        context = data["context_analysis"]
        assert context["escalation"]["detected"] is False
        assert context["escalation"]["rate"] == "none"
    
    def test_analyze_with_empty_history(self, client_with_context):
        """Test analysis with empty message history array."""
        response = client_with_context.post(
            "/analyze",
            json={
                "message": "Hello",
                "message_history": [],
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        
        # Should still work
        assert "crisis_detected" in data


class TestContextResponseFields:
    """Tests for context analysis fields in response."""
    
    def test_escalation_fields(self, client_with_context, base_timestamp):
        """Test escalation section has all required fields."""
        history = create_api_message_history(base_timestamp, count=4)
        
        response = client_with_context.post(
            "/analyze",
            json={
                "message": "I can't cope anymore",
                "message_history": history,
            }
        )
        
        data = response.json()
        escalation = data["context_analysis"]["escalation"]
        
        assert "detected" in escalation
        assert "rate" in escalation
        assert "confidence" in escalation
    
    def test_trend_fields(self, client_with_context, base_timestamp):
        """Test trend section has all required fields."""
        history = create_api_message_history(base_timestamp, count=4)
        
        response = client_with_context.post(
            "/analyze",
            json={
                "message": "Things are getting worse",
                "message_history": history,
            }
        )
        
        data = response.json()
        trend = data["context_analysis"]["trend"]
        
        assert "direction" in trend
        assert "velocity" in trend
    
    def test_temporal_fields(self, client_with_context, base_timestamp):
        """Test temporal section has all required fields."""
        history = create_api_message_history(base_timestamp, count=4)
        
        response = client_with_context.post(
            "/analyze",
            json={
                "message": "Test message",
                "message_history": history,
            }
        )
        
        data = response.json()
        temporal = data["context_analysis"]["temporal"]
        
        assert "late_night_risk" in temporal
        assert "rapid_posting" in temporal
        assert "is_weekend" in temporal
        assert "time_risk_modifier" in temporal
    
    def test_intervention_fields(self, client_with_context, base_timestamp):
        """Test intervention section has all required fields."""
        history = create_api_message_history(base_timestamp, count=4)
        
        response = client_with_context.post(
            "/analyze",
            json={
                "message": "I need help",
                "message_history": history,
            }
        )
        
        data = response.json()
        intervention = data["context_analysis"]["intervention"]
        
        assert "urgency" in intervention
    
    def test_trajectory_fields(self, client_with_context, base_timestamp):
        """Test trajectory section has all required fields."""
        history = create_api_message_history(base_timestamp, count=4)
        
        response = client_with_context.post(
            "/analyze",
            json={
                "message": "Current message",
                "message_history": history,
            }
        )
        
        data = response.json()
        trajectory = data["context_analysis"]["trajectory"]
        
        assert "scores" in trajectory
        assert "start_score" in trajectory
        assert "end_score" in trajectory
        assert "peak_score" in trajectory
    
    def test_history_metadata_fields(self, client_with_context, base_timestamp):
        """Test history metadata section has all required fields."""
        history = create_api_message_history(base_timestamp, count=4)
        
        response = client_with_context.post(
            "/analyze",
            json={
                "message": "Current message",
                "message_history": history,
            }
        )
        
        data = response.json()
        metadata = data["context_analysis"]["history_metadata"]
        
        assert "message_count" in metadata
        assert "time_span_hours" in metadata


class TestMessageHistoryValidation:
    """Tests for message history input validation."""
    
    def test_invalid_timestamp_format(self, client_with_context):
        """Test rejection of invalid timestamp format."""
        response = client_with_context.post(
            "/analyze",
            json={
                "message": "Test",
                "message_history": [
                    {
                        "message": "Previous",
                        "timestamp": "not-a-timestamp",
                        "crisis_score": 0.5,
                    }
                ],
            }
        )
        
        # Should return validation error
        assert response.status_code == 422
    
    def test_invalid_crisis_score(self, client_with_context, base_timestamp):
        """Test rejection of out-of-range crisis score."""
        response = client_with_context.post(
            "/analyze",
            json={
                "message": "Test",
                "message_history": [
                    {
                        "message": "Previous",
                        "timestamp": base_timestamp.isoformat() + "Z",
                        "crisis_score": 1.5,  # Invalid: > 1.0
                    }
                ],
            }
        )
        
        # Should return validation error
        assert response.status_code == 422
    
    def test_empty_message_in_history(self, client_with_context, base_timestamp):
        """Test rejection of empty message in history."""
        response = client_with_context.post(
            "/analyze",
            json={
                "message": "Test",
                "message_history": [
                    {
                        "message": "",  # Empty message
                        "timestamp": base_timestamp.isoformat() + "Z",
                        "crisis_score": 0.5,
                    }
                ],
            }
        )
        
        # Should return validation error
        assert response.status_code == 422
    
    def test_optional_crisis_score(self, client_with_context, base_timestamp):
        """Test that crisis_score is optional in history."""
        response = client_with_context.post(
            "/analyze",
            json={
                "message": "Test",
                "message_history": [
                    {
                        "message": "Previous message",
                        "timestamp": base_timestamp.isoformat() + "Z",
                        # No crisis_score - should be optional
                    }
                ],
            }
        )
        
        # Should succeed
        assert response.status_code == 200
    
    def test_optional_message_id(self, client_with_context, base_timestamp):
        """Test that message_id is optional in history."""
        response = client_with_context.post(
            "/analyze",
            json={
                "message": "Test",
                "message_history": [
                    {
                        "message": "Previous message",
                        "timestamp": base_timestamp.isoformat() + "Z",
                        "crisis_score": 0.5,
                        # No message_id - should be optional
                    }
                ],
            }
        )
        
        # Should succeed
        assert response.status_code == 200


class TestBatchAnalyzeWithHistory:
    """Tests for /analyze/batch endpoint with message history."""
    
    def test_batch_analyze_with_history(self, client_with_context, base_timestamp):
        """Test batch analysis with message history."""
        history = create_api_message_history(base_timestamp, count=3)
        
        response = client_with_context.post(
            "/analyze/batch",
            json={
                "messages": [
                    {
                        "message": "First message",
                        "message_history": history,
                    },
                    {
                        "message": "Second message",
                        "message_history": [],
                    },
                ],
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        
        assert "results" in data
        assert len(data["results"]) == 2


class TestContextConfigEndpoints:
    """Tests for context configuration endpoints."""
    
    def test_get_context_config(self, client_with_context):
        """Test GET /config/context endpoint."""
        response = client_with_context.get("/config/context")
        
        # May return 200 or 501 depending on implementation
        assert response.status_code in [200, 501, 503]
    
    def test_put_context_config(self, client_with_context):
        """Test PUT /config/context endpoint."""
        response = client_with_context.put(
            "/config/context",
            json={
                "enabled": True,
                "max_history_size": 25,
            }
        )
        
        # May return 200 or 501 depending on implementation
        assert response.status_code in [200, 501, 503, 422]


class TestHealthWithContext:
    """Tests for health endpoints with context feature."""
    
    def test_health_endpoint(self, client_with_context):
        """Test health endpoint works with context feature."""
        response = client_with_context.get("/health")
        
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
    
    def test_status_endpoint(self, client_with_context):
        """Test status endpoint works with context feature."""
        response = client_with_context.get("/status")
        
        assert response.status_code == 200
        data = response.json()
        assert "ready" in data or "is_ready" in data


# =============================================================================
# Test Cases: Edge Cases
# =============================================================================


class TestAPIEdgeCases:
    """Tests for API edge cases with context."""
    
    def test_very_long_message(self, client_with_context, base_timestamp):
        """Test handling of very long current message."""
        history = create_api_message_history(base_timestamp, count=3)
        long_message = "Help me please. " * 500  # ~8000 chars
        
        response = client_with_context.post(
            "/analyze",
            json={
                "message": long_message,
                "message_history": history,
            }
        )
        
        assert response.status_code == 200
    
    def test_large_history(self, client_with_context, base_timestamp):
        """Test handling of large message history."""
        history = create_api_message_history(base_timestamp, count=20)
        
        response = client_with_context.post(
            "/analyze",
            json={
                "message": "Current message",
                "message_history": history,
            }
        )
        
        assert response.status_code == 200
    
    def test_unicode_in_history(self, client_with_context, base_timestamp):
        """Test handling of unicode in message history."""
        history = [
            {
                "message": "Feeling 😢 today",
                "timestamp": base_timestamp.isoformat() + "Z",
                "crisis_score": 0.5,
            },
            {
                "message": "Everything is 💔",
                "timestamp": (base_timestamp + timedelta(hours=1)).isoformat() + "Z",
                "crisis_score": 0.6,
            },
        ]
        
        response = client_with_context.post(
            "/analyze",
            json={
                "message": "I can't do this 😞",
                "message_history": history,
            }
        )
        
        assert response.status_code == 200
    
    def test_special_characters_in_history(self, client_with_context, base_timestamp):
        """Test handling of special characters in history."""
        history = [
            {
                "message": "What's wrong? I don't know... <sigh>",
                "timestamp": base_timestamp.isoformat() + "Z",
                "crisis_score": 0.4,
            },
        ]
        
        response = client_with_context.post(
            "/analyze",
            json={
                "message": "I'm \"fine\" (not really)",
                "message_history": history,
            }
        )
        
        assert response.status_code == 200


class TestContextAnalysisIntegration:
    """Full integration tests for context analysis flow."""
    
    def test_full_escalation_flow(self, client_with_context, base_timestamp):
        """Test full flow from escalating history to intervention urgency."""
        # Build escalating history
        history = []
        messages = [
            ("Not my best day", 0.25),
            ("Things are getting harder", 0.4),
            ("I'm really struggling", 0.55),
            ("I don't know what to do", 0.7),
        ]
        
        for i, (msg, score) in enumerate(messages):
            history.append({
                "message": msg,
                "timestamp": (base_timestamp + timedelta(hours=i)).isoformat() + "Z",
                "crisis_score": score,
            })
        
        response = client_with_context.post(
            "/analyze",
            json={
                "message": "I can't take it anymore",
                "message_history": history,
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        
        # Full flow should result in:
        # 1. Crisis detected
        assert data["crisis_detected"] is True
        
        # 2. Context analysis present
        assert "context_analysis" in data
        context = data["context_analysis"]
        
        # 3. Escalation detected
        assert context["escalation"]["detected"] is True
        
        # 4. Worsening trend
        assert context["trend"]["direction"] == "worsening"
        
        # 5. High urgency
        assert context["intervention"]["urgency"] in ["high", "immediate"]
    
    def test_stable_to_crisis_spike(self, client_with_context, base_timestamp):
        """Test sudden crisis spike from stable history."""
        # Stable low history
        history = [
            {
                "message": "Having an okay day",
                "timestamp": (base_timestamp + timedelta(hours=i)).isoformat() + "Z",
                "crisis_score": 0.2,
            }
            for i in range(3)
        ]
        
        response = client_with_context.post(
            "/analyze",
            json={
                "message": "I want to hurt myself",  # Sudden crisis
                "message_history": history,
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        
        # Should detect crisis even without escalation pattern
        assert data["crisis_detected"] is True
        assert data["crisis_score"] > 0.7


# =============================================================================
# Export
# =============================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
