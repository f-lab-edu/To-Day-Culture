from fastapi.testclient import TestClient
from app.main import app
import requests
import time

client = TestClient(app)

# 유저 서비스 호출 함수
def get_user_info(author_id: int):
    try:
        response = requests.get(f"https://user-service:8001/api/users/{author_id}")
        response.raise_for_status()  # 상태 코드가 200이 아닐 경우 HTTPError 발생
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        raise requests.exceptions.HTTPError(f"HTTP error occurred while fetching user info: {http_err}")
    except requests.exceptions.ConnectionError as conn_err:
        raise requests.exceptions.ConnectionError(f"Connection error occurred: {conn_err}")
    except requests.exceptions.Timeout as timeout_err:
        raise requests.exceptions.Timeout(f"Timeout occurred: {timeout_err}")
    except requests.exceptions.RequestException as req_err:
        raise requests.exceptions.RequestException(f"Unexpected error occurred: {req_err}")

# 게시물 생성 테스트
def test_create_post():
    try:
        user_info = get_user_info(1)  # 유저 서비스에서 유저 정보 조회
    except requests.exceptions.RequestException as e:
        assert False, f"유저 정보 조회 실패: {e}"

    response = client.post("/posts/", json={
        "title": "Test Post",
        "content": "This is a test post",
        "author_id": user_info["id"]
    })
    assert response.status_code == 201, f"게시물 생성 실패: {response.json()}"
    assert response.json()["title"] == "Test Post"

# 댓글 추가 테스트
def test_add_comment():
    try:
        user_info = get_user_info(1)
    except requests.exceptions.RequestException as e:
        assert False, f"유저 정보 조회 실패: {e}"

    response = client.post("/posts/1/comments", json={
        "content": "This is a test comment",
        "author_id": user_info["id"]
    })
    assert response.status_code == 201, f"댓글 생성 실패: {response.json()}"
    assert response.json()["content"] == "This is a test comment"

# 게시물 삭제 테스트
def test_delete_post():
    try:
        user_info = get_user_info(1)
    except requests.exceptions.RequestException as e:
        assert False, f"유저 정보 조회 실패: {e}"

    # 게시물 생성
    response = client.post("/posts/", json={
        "title": "Test Post for Delete",
        "content": "This post will be deleted",
        "author_id": user_info["id"]
    })
    assert response.status_code == 201, f"게시물 생성 실패: {response.json()}"

    post_id = response.json().get("id")
    assert post_id is not None, "post_id가 None 입니다."

    # 게시물 존재 여부 확인
    time.sleep(1)  # 데이터베이스 반영 시간 확보
    get_post_response = client.get(f"/posts/{post_id}")
    assert get_post_response.status_code == 200, f"게시물이 생성되지 않았습니다: {get_post_response.json()}"

    # 게시물 삭제 시도
    delete_response = client.delete(f"/posts/{post_id}")
    assert delete_response.status_code == 204, f"게시물 삭제 실패: {delete_response.json()}"

# 댓글 삭제 테스트
def test_delete_comment():
    try:
        user_info = get_user_info(1)
    except requests.exceptions.RequestException as e:
        assert False, f"유저 정보 조회 실패: {e}"

    # 게시물 생성
    response = client.post("/posts/", json={
        "title": "Test Post with Comment",
        "content": "This post has a comment",
        "author_id": user_info["id"]
    })
    assert response.status_code == 201, f"게시물 생성 실패: {response.json()}"
    post_id = response.json()["id"]

    # 댓글 추가
    comment_response = client.post(f"/posts/{post_id}/comments", json={
        "content": "This comment will be deleted",
        "author_id": user_info["id"]
    })
    assert comment_response.status_code == 201, f"댓글 생성 실패: {comment_response.json()}"
    comment_id = comment_response.json()["id"]

    # 댓글 삭제
    delete_comment_response = client.delete(f"/posts/{post_id}/comments/{comment_id}")
    assert delete_comment_response.status_code == 204, f"댓글 삭제 실패: {delete_comment_response.json()}"

# 존재하지 않는 유저로 게시물 생성 시도 테스트
def test_user_not_found():
    response = client.post("/posts/", json={
        "title": "Test Post",
        "content": "This is a test post",
        "author_id": 9999  # 없는 유저 ID
    })
    assert response.status_code == 404, f"유저가 존재하지 않는 경우 게시물 생성 실패: {response.json()}"
    assert response.json()["detail"] == "유저 정보를 가져오는 데 실패했습니다."
