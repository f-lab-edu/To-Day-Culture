from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_post():
    response = client.post("/posts/", json={
        "title": "Test Post",
        "content": "This is a test post",
        "author_id": 1
    })
    assert response.status_code == 201
    assert response.json()["title"] == "Test Post"

def test_add_comment():
    response = client.post("/posts/1/comments", json={
        "content": "This is a test comment",
        "author_id": 1
    })
    assert response.status_code == 201
    assert response.json()["content"] == "This is a test comment"

def test_get_posts():
    response = client.get("/posts/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_delete_post():
    response = client.delete("/posts/1")
    assert response.status_code == 204

def test_delete_comment():
    response = client.delete("/posts/1/comments/1")
    assert response.status_code == 204

def test_user_not_found():
    # 존재하지 않는 유저 정보로 게시물 생성 시도
    response = client.post("/posts/", json={
        "title": "Test Post",
        "content": "This is a test post",
        "author_id": 9999  # 없는 유저 ID
    })
    assert response.status_code == 404
    assert response.json()["detail"] == "유저 정보를 가져오는 데 실패했습니다."
