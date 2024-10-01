# content.py

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
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

# 콘텐츠 목록 조회 엔드포인트
@router.get("/", response_model=list[ContentSchema])
def get_contents(db: Session = Depends(get_db)):
    contents = db.query(Content).all()
    return contents

# 콘텐츠 삭제 엔드포인트
@router.delete("/{content_id}", status_code=204)
def delete_content(content_id: int, db: Session = Depends(get_db)):
    content = db.query(Content).filter(Content.id == content_id).first()
    if content is None:
        raise HTTPException(status_code=404, detail="Content not found")
    db.delete(content)
    db.commit()
