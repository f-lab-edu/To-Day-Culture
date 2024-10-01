from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.schemas import ContentCreate, Content as ContentSchema, ContentFilter
from app.models import Content
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

# 콘텐츠 목록 조회 및 검색/필터링 엔드포인트
@router.get("/", response_model=list[ContentSchema])
def get_contents(
    title: str = Query(None, description="검색할 제목"),
    category: str = Query(None, description="필터링할 카테고리"),
    creator: str = Query(None, description="필터링할 제작자"),
    db: Session = Depends(get_db)
):
    query = db.query(Content)
    
    # 검색 및 필터링 조건 추가
    if title:
        query = query.filter(Content.title.ilike(f"%{title}%"))
    if category:
        query = query.filter(Content.category == category)
    if creator:
        query = query.filter(Content.creator == creator)
    
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
