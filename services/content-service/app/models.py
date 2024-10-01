from sqlalchemy import Column, Integer, String, Text
from app.db import Base

# 콘텐츠 정보를 저장할 데이터베이스 모델 정의
class Content(Base):
    __tablename__ = "contents"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)  # 콘텐츠 제목
    description = Column(Text, nullable=True)    # 콘텐츠 설명
    category = Column(String, nullable=True)  # 선택적 필드로 변경
    creator = Column(String, nullable=True)   # 선택적 필드로 변경