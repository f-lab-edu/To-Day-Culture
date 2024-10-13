from fastapi.testclient import TestClient
from app.main import app
import redis
import json

client = TestClient(app)

# Redis 클라이언트 초기화
redis_client = redis.Redis(host='redis', port=6379, db=0, decode_responses=True)

# 테스트 전에 Redis 캐시를 비움
def setup_function():
    redis_client.flushdb()

# 콘텐츠 생성 테스트
def test_create_content():
    response = client.post("/contents/", json={
        "title": "Test Content",
        "description": "This is a test content",
        "category": "Test",
        "creator": "Tester"
    })
    assert response.status_code == 201
    assert response.json()["title"] == "Test Content"

def test_get_contents_with_existing_id():
    # DB에 존재하는 콘텐츠를 조회하기 위해 미리 콘텐츠 생성
    response = client.post("/contents/", json={
        "title": "Existing Content",
        "description": "This content already exists.",
        "category": "Test",
        "creator": "Tester"
    })
    assert response.status_code == 201
    existing_content_id = response.json()["id"]
    
    # 존재하는 콘텐츠를 조회
    response = client.get(f"/contents/{existing_content_id}")
    assert response.status_code == 200
    assert response.json()["id"] == existing_content_id  # ID가 일치해야 함
    
    # 캐시 확인 (콘텐츠 목록 조회)
    response = client.get("/contents/")
    assert response.status_code == 200
    assert len(response.json()) > 0  # 콘텐츠가 하나 이상 있어야 함

    # 캐시 확인
    cached_data = redis_client.get(f"content_list:None:None")  # 캐시 키 확인
    assert cached_data is not None  # 캐시가 비어있지 않아야 함

# 콘텐츠 삭제 테스트 (캐시 갱신 확인)
def test_delete_content():
    # 새로운 콘텐츠 생성
    response = client.post("/contents/", json={
        "title": "Test Content",
        "description": "This is a test content",
        "category": "Test",
        "creator": "Tester"
    })
    content_id = response.json()["id"]

    # 콘텐츠 삭제
    response = client.delete(f"/contents/{content_id}")
    assert response.status_code == 204

    # 삭제된 콘텐츠 조회 시 404 응답 확인
    get_response = client.get(f"/contents/{content_id}")
    assert get_response.status_code == 404  # 삭제된 콘텐츠에 대해 404를 기대
