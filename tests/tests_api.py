# tests/test_api.py
from fastapi.testclient import TestClient

from api.main import app

client = TestClient(app)

def test_query_endpoint():
    """Test the query endpoint with a simple question"""
    response = client.post(
        "/api/query",
        json={
            "query": "What are Santiago's skills?",
            "conversation_id": None,
            "project_specific": False
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "conversation_id" in data
    assert "response" in data
    assert data["agent_used"] in ["Portfolio Knowledge Expert", "Project Specialist"]
    assert "processing_time" in data