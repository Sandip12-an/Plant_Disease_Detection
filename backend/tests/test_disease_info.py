import pytest
from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)

def test_get_crops_list():
    response = client.get("/api/v1/diseases/crops")
    assert response.status_code == 200
    crops = response.json()
    assert isinstance(crops, list)
    assert len(crops) > 0
    assert any("Tomato" in c for c in crops)

def test_list_diseases():
    response = client.get("/api/v1/diseases?limit=10")
    assert response.status_code == 200
    data = response.json()
    assert "total" in data
    assert "items" in data
    assert len(data["items"]) <= 10

def test_search_diseases():
    response = client.get("/api/v1/diseases?search=blight")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] > 0
    assert any("blight" in item["name"].lower() or "blight" in item["symptoms"].lower() for item in data["items"])

def test_get_disease_detail():
    response = client.get("/api/v1/diseases/Tomato___Early_blight")
    assert response.status_code == 200
    disease = response.json()
    assert disease["id"] == "Tomato___Early_blight"
    assert "Alternaria" in disease["causes"] or "concentric" in disease["symptoms"]
    assert len(disease["organic_treatment"]) > 0
    assert len(disease["prevention"]) > 0
