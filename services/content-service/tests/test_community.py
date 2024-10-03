from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_post():
    response = client.post(
        "/community/posts/",
        json={
            "title": "Test Post",
            "content": "This is a test post content"
        }
    )
    assert response.status_code == 201
    assert response.json()["title"] == "Test Post"

def test_get_posts():
    # 게시글 생성
    client.post(
        "/community/posts/",
        json={
            "title": "Test Post",
            "content": "This is a test post content"
        }
    )

    # 게시글 목록 조회
    response = client.get("/community/posts/")
    assert response.status_code == 200
    assert len(response.json()) > 0

def test_add_comment():
    # 게시글 생성
    post_response = client.post(
        "/community/posts/",
        json={
            "title": "Post with Comment",
            "content": "Post content"
        }
    )
    post_id = post_response.json()["id"]

    # 댓글 추가
    comment_response = client.post(
        f"/community/posts/{post_id}/comments/",
        json={
            "content": "This is a comment"
        }
    )
    assert comment_response.status_code == 201
    assert comment_response.json()["content"] == "This is a comment"

def test_delete_post():
    # 게시글 생성
    post_response = client.post(
        "/community/posts/",
        json={
            "title": "Post to Delete",
            "content": "Post content"
        }
    )
    post_id = post_response.json()["id"]

    # 게시글 삭제
    delete_response = client.delete(f"/community/posts/{post_id}")
    assert delete_response.status_code == 204
