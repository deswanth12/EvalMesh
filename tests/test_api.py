import pytest
from fastapi.testclient import TestClient
from evalmesh.proxy import app

client = TestClient(app)

def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_reliability_score_endpoint():
    response = client.get("/api/reliability")
    assert response.status_code == 200
    assert response.json()["score"] == 94

def test_incidents_endpoint():
    response = client.get("/api/incidents")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_agents_endpoint():
    response = client.get("/api/agents")
    assert response.status_code == 200
    assert len(response.json()) >= 1
