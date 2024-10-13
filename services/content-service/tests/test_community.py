import time
import requests
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# 유저 서비스 호출 함수
def get_user_info(author_id: int):
    try:
        response = requests.get(f"https://user-service:8001/api/users/{author_id}")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise e

# 게시물 생성 테스트
def test_create_post():
    user_info = get_user_info(1)  # 유저 서비스에서 유저 정보 조회
    response = client.post("/posts/", json={
        "title": "Test Post",
        "content": "This is a test post",
        "author_id": user_info["id"]
    })
    assert response.status_code == 201
    assert response.json()["title"] == "Test Post"

# 댓글 추가 테스트
def test_add_comment():
    user_info = get_user_info(1)
    response = client.post("/posts/1/comments", json={
        "content": "This is a test comment",
        "author_id": user_info["id"]
    })
    assert response.status_code == 201
    assert response.json()["content"] == "This is a test comment"

# 게시물 삭제 테스트
def test_delete_post():
    user_info = get_user_info(1)

    # 게시물 생성
    response = client.post("/posts/", json={
        "title": "Test Post for Delete",
        "content": "This post will be deleted",
        "author_id": user_info["id"]
    })
    assert response.status_code == 201
    post_id = response.json().get("id")
    assert post_id is not None

    # 게시물 존재 여부 확인
    time.sleep(1)  # 데이터베이스 반영 시간 확보
    get_post_response = client.get(f"/posts/{post_id}")
    assert get_post_response.status_code == 200

    # 게시물 삭제 시도
    delete_response = client.delete(f"/posts/{post_id}")
    assert delete_response.status_code == 204

# 댓글 삭제 테스트
def test_delete_comment():
    user_info = get_user_info(1)

    # 게시물 생성
    response = client.post("/posts/", json={
        "title": "Test Post with Comment",
        "content": "This post has a comment",
        "author_id": user_info["id"]
    })
    assert response.status_code == 201
    post_id = response.json()["id"]

    # 댓글 추가
    comment_response = client.post(f"/posts/{post_id}/comments", json={
        "content": "This comment will be deleted",
        "author_id": user_info["id"]
    })
    assert comment_response.status_code == 201
    comment_id = comment_response.json()["id"]

    # 댓글 삭제
    delete_comment_response = client.delete(f"/posts/{post_id}/comments/{comment_id}")
    assert delete_comment_response.status_code == 204

# 존재하지 않는 유저로 게시물 생성 시도 테스트
def test_user_not_found():
    response = client.post("/posts/", json={
        "title": "Test Post",
        "content": "This is a test post",
        "author_id": 9999  # 없는 유저 ID
    })
    assert response.status_code == 404
    assert response.json()["detail"] == "유저 정보를 가져오는 데 실패했습니다."
