import pytest
from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)

def test_health_probe():
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "model_engine" in data

def test_user_registration_and_login():
    test_email = "farmer_test@example.com"
    test_password = "SecurePassword123!"

    # 1. Register
    reg_response = client.post(
        "/api/v1/auth/register",
        json={"email": test_email, "password": test_password, "full_name": "Test Farmer"}
    )
    assert reg_response.status_code in [201, 400] # 400 if already created in previous run

    # 2. Login
    login_response = client.post(
        "/api/v1/auth/login",
        json={"email": test_email, "password": test_password}
    )
    assert login_response.status_code == 200
    token_data = login_response.json()
    assert "access_token" in token_data
    assert token_data["token_type"] == "bearer"

    # 3. Authenticated profile check
    token = token_data["access_token"]
    me_response = client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert me_response.status_code == 200
    assert me_response.json()["email"] == test_email
