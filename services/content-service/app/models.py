# models.py
from sqlalchemy import Column, Integer, String, Text, Index
from app.db import Base

# 콘텐츠 정보를 저장할 데이터베이스 모델 정의
class Content(Base):
    __tablename__ = "contents"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False, index=True)  # 인덱스 추가
    description = Column(Text, nullable=True)
    category = Column(String, nullable=True, index=True)  # 인덱스 추가
    creator = Column(String, nullable=True, index=True)  # 인덱스 추가

# 복합 인덱스 추가
Index('idx_title_category', Content.title, Content.category)
