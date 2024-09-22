from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.models import Content
from app.schemas import ContentCreate, Content as ContentSchema
from app.db import get_db

# 콘텐츠 관련 API 엔드포인트들을 관리할 라우터
router = APIRouter()

# 콘텐츠 생성 엔드포인트
@router.post("/", response_model=ContentSchema, status_code=status.HTTP_201_CREATED)
def create_content(content: ContentCreate, db: Session = Depends(get_db)):
    db_content = Content(**content.dict())
    db.add(db_content)
    db.commit()
    db.refresh(db_content)
    return db_content

# 전체 콘텐츠 조회 엔드포인트
@router.get("/", response_model=list[ContentSchema])
def get_contents(db: Session = Depends(get_db)):
    return db.query(Content).all()

# 특정 콘텐츠 조회 엔드포인트
@router.get("/{content_id}", response_model=ContentSchema)
def get_content(content_id: int, db: Session = Depends(get_db)):
    db_content = db.query(Content).filter(Content.id == content_id).first()
    if db_content is None:
        raise HTTPException(status_code=404, detail="Content not found")
    return db_content

# 콘텐츠 삭제 엔드포인트
@router.delete("/{content_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_content(content_id: int, db: Session = Depends(get_db)):
    db_content = db.query(Content).filter(Content.id == content_id).first()
    if db_content is None:
        raise HTTPException(status_code=404, detail="Content not found")
    db.delete(db_content)
    db.commit()
    return None
