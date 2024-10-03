# content.py
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.schemas import ContentCreate, Content as ContentSchema
from app.models import Content
from app.schemas import PostCreate, Post, CommentCreate, Comment
from app.models import Post as PostModel, Comment as CommentModel
from app.db import get_db

router = APIRouter()

# 콘텐츠 생성 엔드포인트
@router.post("/", response_model=ContentSchema, status_code=201)
def create_content(content: ContentCreate, db: Session = Depends(get_db)):
    new_content = Content(
        title=content.title,
        description=content.description,
        category=content.category,
        creator=content.creator
    )
    db.add(new_content)
    db.commit()
    db.refresh(new_content)
    return new_content

# 콘텐츠 목록 조회 엔드포인트 (필터링 기능 추가)
@router.get("/", response_model=list[ContentSchema])
def get_contents(title: str = None, category: str = None, db: Session = Depends(get_db)):
    query = db.query(Content)

    if title:
        query = query.filter(Content.title.ilike(f"%{title}%"))
    if category:
        query = query.filter(Content.category == category)
    
    contents = query.all()
    return contents

# 콘텐츠 삭제 엔드포인트
@router.delete("/{content_id}", status_code=204)
def delete_content(content_id: int, db: Session = Depends(get_db)):
    content = db.query(Content).filter(Content.id == content_id).first()
    if content is None:
        raise HTTPException(status_code=404, detail="Content not found")
    db.delete(content)
    db.commit()

# 게시글 생성 API
@router.post("/posts/", response_model=Post, status_code=201)
def create_post(post: PostCreate, db: Session = Depends(get_db)):
    new_post = PostModel(title=post.title, content=post.content, author_id=1)  # 현재는 하드코딩된 사용자 ID
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

# 게시글 목록 조회 API
@router.get("/posts/", response_model=list[Post])
def get_posts(db: Session = Depends(get_db)):
    return db.query(PostModel).all()

# 게시글 ID로 단일 게시글 조회 API
@router.get("/posts/{post_id}", response_model=Post)
def get_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(PostModel).filter(PostModel.id == post_id).first()
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return post

# 게시글에 댓글 추가 API
@router.post("/posts/{post_id}/comments/", response_model=Comment, status_code=201)
def add_comment(post_id: int, comment: CommentCreate, db: Session = Depends(get_db)):
    new_comment = CommentModel(content=comment.content, post_id=post_id, author_id=1)
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment

# 게시글 삭제 API
@router.delete("/posts/{post_id}", status_code=204)
def delete_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(PostModel).filter(PostModel.id == post_id).first()
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    db.delete(post)
    db.commit()