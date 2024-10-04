import requests
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.models import Post, Comment
from app.schemas import PostCreate, PostResponse, CommentCreate, CommentResponse
from app.db import get_db

router = APIRouter()

# 사용자 정보 가져오기 함수
def get_user_info(author_id: int):
    try:
        # 유저 서비스 API 호출
        response = requests.get(f"http://localhost:8001/api/users/{author_id}")
        if response.status_code == 200:
            return response.json()  # 유저 정보 반환
        else:
            raise HTTPException(status_code=response.status_code, detail="유저 정보를 가져오는 데 실패했습니다.")
    except requests.exceptions.RequestException as e:
        # 유저 서비스와의 통신 실패 시 예외 처리
        print(f"유저 서비스와의 통신 오류: {e}")
        raise HTTPException(status_code=500, detail="유저 서비스와의 연결에 실패했습니다.")

# 게시물 생성 엔드포인트
@router.post("/posts/", response_model=PostResponse, status_code=201)
def create_post(post: PostCreate, db: Session = Depends(get_db)):
    # author_id 검증 (user-service로 API 호출)
    user_info = get_user_info(post.author_id)

    # 게시물 생성
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
@router.post("/posts/{post_id}/comments", response_model=CommentResponse, status_code=201)
def add_comment(post_id: int, comment: CommentCreate, db: Session = Depends(get_db)):
    # author_id 검증 (user-service로 API 호출)
    user_info = get_user_info(comment.author_id)

    # 게시물 존재 여부 확인
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

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

# 게시물 목록 조회 엔드포인트
@router.get("/posts/", response_model=list[PostResponse])
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(Post).all()
    return posts

# 게시물 삭제 엔드포인트
@router.delete("/posts/{post_id}", status_code=204)
def delete_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    db.delete(post)
    db.commit()

# 댓글 삭제 엔드포인트
@router.delete("/posts/{post_id}/comments/{comment_id}", status_code=204)
def delete_comment(post_id: int, comment_id: int, db: Session = Depends(get_db)):
    comment = db.query(Comment).filter(Comment.id == comment_id, Comment.post_id == post_id).first()
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    db.delete(comment)
    db.commit()
