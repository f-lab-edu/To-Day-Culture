# tests/test_content.py

from fastapi.testclient import TestClient
from app.main import app  # FastAPI 앱을 임포트

# TestClient 생성
client = TestClient(app)

def test_create_content():
    response = client.post(
        "/contents/",
        json={
            "title": "Test Movie",
            "description": "A great movie",
            "category": "Movie",  # 필수 필드 추가
            "creator": "John Doe"  # 필수 필드 추가
        }
    )
    assert response.status_code == 201
    assert response.json()["title"] == "Test Movie"


def test_get_content():
    # 콘텐츠 생성
    response = client.post(
        "/contents/",
        json={
            "title": "Test Performance",
            "description": "A live performance",
            "category": "Performance",  # 필수 필드 추가
            "creator": "Jane Smith"  # 필수 필드 추가
        }
    )
    content_id = response.json()["id"]
    
    # 콘텐츠 목록 조회
    response = client.get("/contents/")
    assert response.status_code == 200
    contents = response.json()
    assert len(contents) > 0
    assert any(content["title"] == "Test Performance" for content in contents)


def test_delete_content():
    # 콘텐츠 생성
    response = client.post(
        "/contents/",
        json={
            "title": "Test Art",
            "description": "An amazing art",
            "category": "Art",  # 필수 필드 추가
            "creator": "John Artist"  # 필수 필드 추가
        }
    )
    content_id = response.json()["id"]
    
    # 콘텐츠 삭제
    response = client.delete(f"/contents/{content_id}")
    assert response.status_code == 204
