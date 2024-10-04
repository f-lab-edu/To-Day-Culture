from fastapi.testclient import TestClient
from app.main import app
import uuid

client = TestClient(app)

def create_test_user():
    """고유한 이메일을 생성하여 테스트 사용자 생성"""
    email = f"testuser{uuid.uuid4()}@example.com"
    response = client.post(
        "/auth/signup",
        json={
            "email": email,
            "password": "testpassword",
            "username": "testuser"
        }
    )
    assert response.status_code == 201, f"회원가입 실패: {response.json()}"
    
    # 유저가 정상적으로 생성된 후 ID를 반환
    user_id = response.json()["id"]
    return email, user_id

def test_signup():
    """새로운 사용자 회원가입 테스트"""
    response = client.post(
        "/auth/signup",
        json={
            "email": f"newtestuser{uuid.uuid4()}@example.com",
            "password": "newpassword",
            "username": "newtestuser"
        }
    )
    assert response.status_code == 201, f"회원가입 실패: {response.json()}"

def test_login():
    """로그인 테스트"""
    # 테스트용 사용자 생성
    email, _ = create_test_user()

    # 로그인 요청
    response = client.post(
        "/auth/login",
        json={
            "email": email,
            "password": "testpassword"
        }
    )
    
    # 로그인 성공 여부 확인
    assert response.status_code == 200, f"로그인 실패: {response.json()}"
    assert "access_token" in response.json(), "액세스 토큰이 응답에 포함되지 않음"
    token = response.json()["access_token"]
    return token

def test_protected_route():
    """로그인 후 보호된 엔드포인트 접근 테스트"""
    token = test_login()

    # 보호된 엔드포인트에 접근
    protected_response = client.get(
        "/auth/protected-endpoint",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    # 보호된 엔드포인트 접근 성공 여부 확인
    assert protected_response.status_code == 200, f"보호된 엔드포인트 접근 실패: {protected_response.json()}"
    assert "안녕하세요" in protected_response.json()["msg"], "보호된 엔드포인트 메시지가 예상과 다릅니다."


