from fastapi import FastAPI
from app.auth import router as auth_router

app = FastAPI()

# 회원가입 및 로그인 라우터 등록
app.include_router(auth_router, prefix="/auth")