# main.py
from fastapi import FastAPI
from app.content import router as content_router
from app.community import router as community_router

app = FastAPI()

# 콘텐츠 서비스 라우터 추가
app.include_router(content_router, prefix="/contents", tags=["contents"])

# 라우터 등록
app.include_router(community_router, prefix="/posts", tags=["community"])
app.include_router(content_router, prefix="/contents", tags=["content"])
# 추가적인 라우터나 미들웨어 설정이 여기에 들어갈 수 있습니다.
