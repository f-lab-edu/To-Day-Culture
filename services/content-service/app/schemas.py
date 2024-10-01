from pydantic import BaseModel
from typing import Optional

# 콘텐츠 생성 시 사용할 스키마
class ContentCreate(BaseModel):
    title: str
    description: str
    category: str  # 필수 필드
    creator: str   # 필수 필드

# 콘텐츠 조회 및 반환 스키마
class Content(ContentCreate):
    id: int

    class Config:
        from_attributes = True

# 검색 및 필터링 시 사용할 스키마
class ContentFilter(BaseModel):
    title: Optional[str] = None
    category: Optional[str] = None
    creator: Optional[str] = None
