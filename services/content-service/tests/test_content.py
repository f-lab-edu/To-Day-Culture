# test_content.py
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
            "category": "Movie",
            "creator": "John Doe"
        }
    )
    assert response.status_code == 201
    assert response.json()["title"] == "Test Movie"


def test_get_content():
    # 콘텐츠 생성 후 상태 확인
    client.post(
        "/contents/",
        json={
            "title": "Test Performance",
            "description": "A live performance",
            "category": "Performance",
            "creator": "Jane Smith"
        }
    )
    
    # 제목 필터링 테스트
    response = client.get("/contents/?title=Test")
    assert response.status_code == 200
    contents = response.json()
    assert len(contents) > 0
    assert any(content["title"] == "Test Performance" for content in contents)

    # 카테고리 필터링 테스트
    response = client.get("/contents/?category=Performance")
    assert response.status_code == 200
    contents = response.json()
    assert any(content["category"] == "Performance" for content in contents)


def test_delete_content():
    # 콘텐츠 생성
    response = client.post(
        "/contents/",
        json={
            "title": "Test Art",
            "description": "An amazing art",
            "category": "Art",
            "creator": "John Artist"
        }
    )
    content_id = response.json()["id"]
    
    # 콘텐츠 삭제
    response = client.delete(f"/contents/{content_id}")
    assert response.status_code == 204
