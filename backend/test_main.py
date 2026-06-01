from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_fetch_currencies_endpoint():
    response = client.post("/currencies/fetch")
    assert response.status_code == 200
    
    data = response.json()
    assert "status" in data
    assert data["status"] == "success"

def test_get_currencies_list():
    response = client.get("/currencies")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_currencies_by_date():
    client.post("/currencies/fetch")
    
    fetch_response = client.post("/currencies/fetch").json()
    test_date = fetch_response["date"]
    
    response = client.get(f"/currencies/{test_date}")
    assert response.status_code == 200
    
    data = response.json()
    assert isinstance(data, list)
    if len(data) > 0:
        assert data[0]["date"] == test_date