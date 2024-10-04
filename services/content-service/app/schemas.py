from pydantic import BaseModel
from typing import Optional, List

# 콘텐츠 생성 시 사용할 스키마
class ContentCreate(BaseModel):
    title: str
    description: Optional[str]
    category: Optional[str]
    creator: str

class Content(BaseModel):
    id: int
    title: str
    description: Optional[str]
    category: Optional[str]
    creator: str

    class Config:
        orm_mode = True


# 커뮤니티(Post, Comment) 관련 스키마 정의
class PostCreate(BaseModel):
    title: str
    content: str
    author_id: int

class PostResponse(PostCreate):
    id: int

    class Config:
        orm_mode = True

class CommentCreate(BaseModel):
    content: str
    author_id: int

class CommentResponse(CommentCreate):
    id: int
    post_id: int

    class Config:
        orm_mode = True
