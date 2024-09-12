import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.auth import fake_users_db

client = TestClient(app)

@pytest.fixture(autouse=True)
def reset_fake_users_db():
    fake_users_db.clear()


def test_signup_success():
    response = client.post(
        "/auth/signup",
        json={
            "email": "testuser@example.com",
            "username": "testuser",
            "password": "password123"
        }
    )
    assert response.status_code == 201
    assert response.json() == {"msg": "회원가입이 완료되었습니다."}


def test_signup_duplicate_email():
    client.post(
        "/auth/signup",
        json={
            "email": "testuser@example.com",
            "username": "testuser1",
            "password": "password123"
        }
    )
    response = client.post(
        "/auth/signup",
        json={
            "email": "testuser@example.com",
            "username": "testuser2",
            "password": "password456"
        }
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "이미 가입된 이메일입니다."}


def test_signup_invalid_email_format():
    response = client.post(
        "/auth/signup",
        json={
            "email": "invalid-email-format",
            "username": "testuser",
            "password": "password123"
        }
    )
    assert response.status_code == 422  # FastAPI는 자동으로 422를 반환


def test_login_success():
    client.post(
        "/auth/signup",
        json={
            "email": "testuser@example.com",
            "username": "testuser",
            "password": "password123"
        }
    )
    response = client.post(
        "/auth/login",
        json={
            "email": "testuser@example.com",
            "password": "password123"
        }
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"


def test_login_invalid_credentials():
    client.post(
        "/auth/signup",
        json={
            "email": "testuser@example.com",
            "username": "testuser",
            "password": "password123"
        }
    )
    response = client.post(
        "/auth/login",
        json={
            "email": "testuser@example.com",
            "password": "wrongpassword"
        }
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "이메일 또는 비밀번호가 잘못되었습니다."}


def test_login_non_existent_email():
    response = client.post(
        "/auth/login",
        json={
            "email": "nonexistent@example.com",
            "password": "password123"
        }
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "이메일 또는 비밀번호가 잘못되었습니다."}
