from sqlalchemy import Column, Integer, String, Text
from app.db import Base

# 콘텐츠 정보를 저장할 데이터베이스 모델 정의
class Content(Base):
    __tablename__ = "contents"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)  # 콘텐츠 제목
    description = Column(Text, nullable=True)    # 콘텐츠 설명
    category = Column(String(50), nullable=False)  # 콘텐츠 카테고리 (예: 영화, 공연, 뮤지컬 등)
    creator = Column(String(100), nullable=False)  # 제작자 정보
