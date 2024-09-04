from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# 회원가입 테스트
def test_signup():
    response = client.post(
        "/auth/signup",
        json={
            "email": "test@example.com",
            "username": "testuser",
            "password": "testpassword"
        }
    )
    assert response.status_code == 201
    assert response.json() == {"msg": "User created successfully"}

# 로그인 테스트
def test_login():
    # 먼저 회원가입
    client.post(
        "/auth/signup",
        json={
            "email": "test@example.com",
            "username": "testuser",
            "password": "testpassword"
        }
    )

    # 로그인 테스트
    response = client.post(
        "/auth/login",
        json={
            "email": "test@example.com",
            "password": "testpassword"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

# 보호된 API 테스트
def test_protected_route():
    # 회원가입 및 로그인
    client.post(
        "/auth/signup",
        json={
            "email": "test@example.com",
            "username": "testuser",
            "password": "testpassword"
        }
    )
    
    login_response = client.post(
        "/auth/login",
        json={
            "email": "test@example.com",
            "password": "testpassword"
        }
    )
    
    token = login_response.json()["access_token"]

    # 보호된 엔드포인트 접근
    response = client.get(
        "/protected-endpoint", 
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 200
    assert response.json() == {"email": "test@example.com", "message": "This is a protected route"}
