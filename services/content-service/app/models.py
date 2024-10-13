from sqlalchemy import Column, Integer, String, Text, Index, ForeignKey
from sqlalchemy.orm import relationship
from app.db import Base

# 콘텐츠 정보를 저장할 데이터베이스 모델 정의
class Content(Base):
    __tablename__ = "contents"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False, index=True)  # 인덱스 추가
    description = Column(Text, nullable=True)
    category = Column(String, nullable=True, index=True)  # 인덱스 추가
    creator = Column(String, nullable=True, index=True)  # 인덱스 추가

    # 콘텐츠를 딕셔너리로 변환하는 메서드 추가
    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "category": self.category,
            "creator": self.creator
        }

# 복합 인덱스 추가
Index('idx_title_category', Content.title, Content.category)

class Post(Base):
    __tablename__ = "posts"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(String)
    author_id = Column(Integer)
    
    # 댓글 관계 설정
    comments = relationship("Comment", back_populates="post", cascade="all, delete-orphan")

class Comment(Base):
    __tablename__ = "comments"
    
    id = Column(Integer, primary_key=True, index=True)
    content = Column(String)
    author_id = Column(Integer)
    post_id = Column(Integer, ForeignKey("posts.id"))
    
    # 게시물과의 관계 설정
    post = relationship("Post", back_populates="comments")
