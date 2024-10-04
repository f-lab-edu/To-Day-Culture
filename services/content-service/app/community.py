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

# 사용자 정보 가져오기 함수
def get_user_info(author_id: int):
    try:
        # HTTP -> HTTPS로 변경하여 보안 강화
        response = requests.get(f"https://user-service:8001/api/users/{author_id}")
        if response.status_code == 200:
            return response.json()
        else:
            raise HTTPException(status_code=response.status_code, detail=USER_SERVICE_ERROR)
    except requests.exceptions.RequestException as e:
        print(f"유저 서비스와의 통신 오류: {e}")
        raise HTTPException(status_code=500, detail="유저 서비스와의 연결에 실패했습니다.")

# 게시물 생성 엔드포인트
@router.post("/", response_model=PostResponse, status_code=201)
def create_post(post: PostCreate, db: Session = Depends(get_db)):
    # 유저 정보 가져오기, 실제로 사용할 경우에만 가져옴
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
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail=POST_NOT_FOUND)
    
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
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail=POST_NOT_FOUND)
    return post

# 게시물 삭제 엔드포인트
@router.delete("/posts/{post_id}", status_code=204)
def delete_post(post_id: int, db: Session = Depends(get_db)):
    # 게시물 존재 여부 확인
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail=POST_NOT_FOUND)
    
    # 게시물 삭제 (관련된 댓글도 함께 삭제됨)
    db.delete(post)
    db.commit()
    return {"msg": "Post deleted successfully"}

# 댓글 삭제 엔드포인트
@router.delete("/{post_id}/comments/{comment_id}", status_code=204)
def delete_comment(post_id: int, comment_id: int, db: Session = Depends(get_db)):
    # 댓글 존재 여부 확인
    comment = db.query(Comment).filter(Comment.id == comment_id, Comment.post_id == post_id).first()
    if not comment:
        raise HTTPException(status_code=404, detail=COMMENT_NOT_FOUND)
    
    # 댓글 삭제
    db.delete(comment)
    db.commit()
