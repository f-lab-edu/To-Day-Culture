from fastapi import FastAPI
from app.db import Base, engine
from app.content import router as content_router

# FastAPI 애플리케이션 생성
app = FastAPI()

# 데이터베이스 테이블 자동 생성
Base.metadata.create_all(bind=engine)

# 콘텐츠 API 라우터 등록
app.include_router(content_router, prefix="/contents", tags=["contents"])
