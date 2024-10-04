from fastapi import FastAPI
from app.content import router as content_router
from app.community import router as community_router

app = FastAPI()

# 콘텐츠 서비스 라우터 추가
app.include_router(content_router, prefix="/contents", tags=["contents"])

# 커뮤니티 서비스 라우터 추가
app.include_router(community_router, prefix="/posts", tags=["community"])
