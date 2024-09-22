import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_signup():
    response = client.post(
        "/auth/signup",
        json={
            "email": "newtestuser1@example.com",
            "username": "testuser",
            "password": "testpassword"
        }
    )
    assert response.status_code == 201
    assert response.json() == {"msg": "회원가입이 완료되었습니다."}

def test_login():
    response = client.post(
        "/auth/login",
        json={
            "email": "testuser@example.com",
            "password": "testpassword"
        }
    )
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_protected_route():
    login_response = client.post(
        "/auth/login",
        json={
            "email": "testuser@example.com",
            "password": "testpassword"
        }
    )
    token = login_response.json()["access_token"]
    
    protected_response = client.get(
        "/auth/protected-endpoint",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert protected_response.status_code == 200
    assert "안녕하세요" in protected_response.json()["msg"]
