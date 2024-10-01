# main.py
from fastapi import FastAPI
from app.content import router as content_router

app = FastAPI()

# 콘텐츠 서비스 라우터 추가
app.include_router(content_router, prefix="/contents", tags=["contents"])

# 추가적인 라우터나 미들웨어 설정이 여기에 들어갈 수 있습니다.
