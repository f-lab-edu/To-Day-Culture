import requests
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.models import Post, Comment
from app.schemas import PostCreate, PostResponse, CommentCreate, CommentResponse
from app.db import get_db

router = APIRouter()

# 상수 정의
POST_NOT_FOUND = "Post not found"
COMMENT_NOT_FOUND = "Comment not found"
USER_SERVICE_ERROR = "유저 정보를 가져오는 데 실패했습니다."
USER_SERVICE_CONNECTION_FAILED = "유저 서비스와의 연결에 실패했습니다."
USER_SERVICE_TIMEOUT = "유저 서비스 타임아웃"
USER_SERVICE_COMMUNICATION_ERROR = "유저 서비스와의 통신 오류"
POST_DELETED_SUCCESS = "Post deleted successfully"

# 사용자 정보 가져오기 함수
def get_user_info(author_id: int):
    try:
        response = requests.get(f"https://user-service:8001/api/users/{author_id}")
        response.raise_for_status()  # 상태 코드가 200이 아닐 경우 HTTPError를 발생시킴
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        raise HTTPException(status_code=response.status_code, detail=USER_SERVICE_ERROR) from http_err
    except requests.exceptions.ConnectionError as conn_err:
        print(f"유저 서비스와의 연결 오류: {conn_err}")
        raise HTTPException(status_code=500, detail=USER_SERVICE_CONNECTION_FAILED) from conn_err
    except requests.exceptions.Timeout as timeout_err:
        print(f"유저 서비스 타임아웃: {timeout_err}")
        raise HTTPException(status_code=504, detail=USER_SERVICE_TIMEOUT) from timeout_err
    except requests.exceptions.RequestException as req_err:
        print(f"유저 서비스 통신 오류: {req_err}")
        raise HTTPException(status_code=500, detail=USER_SERVICE_COMMUNICATION_ERROR) from req_err

# 게시물 존재 여부 확인 함수 (중복 제거)
def get_post_or_404(post_id: int, db: Session):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail=POST_NOT_FOUND)
    return post

# 게시물 생성 엔드포인트
@router.post("/", response_model=PostResponse, status_code=201)
def create_post(post: PostCreate, db: Session = Depends(get_db)):
    # 유저 정보 가져오기
    get_user_info(post.author_id)

    new_post = Post(
        title=post.title,
        content=post.content,
        author_id=post.author_id
    )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

# 댓글 추가 엔드포인트
@router.post("/{post_id}/comments", response_model=CommentResponse, status_code=201)
def add_comment(post_id: int, comment: CommentCreate, db: Session = Depends(get_db)):
    # 유저 정보 가져오기
    get_user_info(comment.author_id)

    # 게시물 존재 여부 확인
    post = get_post_or_404(post_id, db)

    # 댓글 생성
    new_comment = Comment(
        content=comment.content,
        author_id=comment.author_id,
        post_id=post_id
    )
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment

# 게시물 조회 엔드포인트
@router.get("/posts/{post_id}", response_model=PostResponse)
def get_post(post_id: int, db: Session = Depends(get_db)):
    return get_post_or_404(post_id, db)

# 게시물 삭제 엔드포인트
@router.delete("/posts/{post_id}", status_code=204)
def delete_post(post_id: int, db: Session = Depends(get_db)):
    # 게시물 존재 여부 확인
    post = get_post_or_404(post_id, db)

    # 게시물 삭제 (관련된 댓글도 함께 삭제됨)
    db.delete(post)
    db.commit()
    return {"msg": POST_DELETED_SUCCESS}

# 댓글 삭제 엔드포인트
@router.delete("/{post_id}/comments/{comment_id}", status_code=204)
def delete_comment(post_id: int, comment_id: int, db: Session = Depends(get_db)):
    # 게시물과 댓글 존재 여부 확인
    get_post_or_404(post_id, db)
    
    comment = db.query(Comment).filter(Comment.id == comment_id, Comment.post_id == post_id).first()
    if not comment:
        raise HTTPException(status_code=404, detail=COMMENT_NOT_FOUND)
    
    # 댓글 삭제
    db.delete(comment)
    db.commit()
