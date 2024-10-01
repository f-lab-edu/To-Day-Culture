# content.py
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.schemas import ContentCreate, Content as ContentSchema
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

# 콘텐츠 목록 조회 엔드포인트 (필터링 기능 추가)
@router.get("/", response_model=list[ContentSchema])
def get_contents(title: str = None, category: str = None, db: Session = Depends(get_db)):
    query = db.query(Content.id, Content.title, Content.category)  # 필요한 필드만 선택적으로 조회

    if title:
        query = query.filter(Content.title.ilike(f"%{title}%"))  # 제목에 대한 필터링
    if category:
        query = query.filter(Content.category == category)  # 카테고리에 대한 필터링
    
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
