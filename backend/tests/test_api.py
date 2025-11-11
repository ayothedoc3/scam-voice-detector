"""API endpoint tests"""
from fastapi.testclient import TestClient
from app.main import app
import pytest
import os

client = TestClient(app)

def test_health_check():
    """Test health check endpoint"""
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "service" in data
    assert "version" in data

def test_analyze_endpoint_no_file():
    """Test analyze endpoint without file"""
    response = client.post("/api/v1/analyze")
    assert response.status_code == 422  # Validation error

def test_analyze_endpoint_invalid_format():
    """Test analyze endpoint with invalid file format"""
    files = {'file': ('test.txt', b'invalid content', 'text/plain')}
    response = client.post("/api/v1/analyze", files=files)
    assert response.status_code == 400

# Add more tests for valid audio files when sample files are available
