from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_fetch_currencies_endpoint():
    response = client.post("/currencies/fetch")
    
    
    assert response.status_code == 200
    
   
    data = response.json()
    assert "status" in data
    assert data["status"] == "success"