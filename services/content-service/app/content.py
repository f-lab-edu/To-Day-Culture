# content.py
import json
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.schemas import ContentCreate, Content as ContentSchema
from app.models import Content
from app.db import get_db
import redis

router = APIRouter()

redis_client = redis.Redis(host='redis', port=6379, db=0, decode_responses=True)
CACHE_TTL = 3600

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
    
    redis_client.delete("content_list")  # 캐시 삭제

    return new_content

@router.get("/", response_model=list[ContentSchema])
def get_contents(title: str = None, category: str = None, db: Session = Depends(get_db)):
    redis_key = f"content_list:{title}:{category}"

    cached_data = redis_client.get(redis_key)
    if cached_data:
        return json.loads(cached_data)

    query = db.query(Content)
    if title:
        query = query.filter(Content.title.ilike(f"%{title}%"))
    if category:
        query = query.filter(Content.category == category)
    
    contents = query.all()

    # 헬퍼 메서드를 사용하여 데이터를 JSON으로 변환
    redis_client.setex(redis_key, CACHE_TTL, json.dumps([content.to_dict() for content in contents]))

    return contents

@router.delete("/{content_id}", status_code=204)
def delete_content(content_id: int, db: Session = Depends(get_db)):
    content = db.query(Content).filter(Content.id == content_id).first()
    if content is None:
        raise HTTPException(status_code=404, detail="Content not found")
    
    db.delete(content)
    db.commit()

    redis_client.delete("content_list")  # 캐시 삭제