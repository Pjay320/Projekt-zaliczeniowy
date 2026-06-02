import pytest
from fastapi.testclient import TestClient
from main import app
from database import SessionLocal

client = TestClient(app)


def test_database_connection():
    try:
        db = SessionLocal()
        assert db is not None
        db.close()
    except Exception as e:
        pytest.fail(f"Połączenie z bazą danych nie powiodło się: {e}")


def test_get_stats_valid_response():
    
    response = client.get("/currencies/stats?start_date=2026-05-01&end_date=2026-05-31")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_stats_missing_parameters():
    
    response = client.get("/currencies/stats")
    assert response.status_code == 422