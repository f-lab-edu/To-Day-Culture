# schemas.py

from pydantic import BaseModel

class ContentCreate(BaseModel):
    title: str
    description: str
    category: str  # 필수 필드로 설정
    creator: str   # 필수 필드로 설정

class Content(ContentCreate):
    id: int

    class Config:
        from_attributes = True
