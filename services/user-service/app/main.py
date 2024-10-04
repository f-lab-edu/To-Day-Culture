from fastapi import FastAPI
from app.auth import router as auth_router
from app.db import Base, engine

app = FastAPI()

# 데이터베이스 테이블 생성
Base.metadata.create_all(bind=engine)

# 회원가입 및 로그인 라우터 등록
app.include_router(auth_router, prefix="/auth")

# 건강 체크 엔드포인트
@app.get("/")
def read_root():
    return {"message": "To-Day Culture API is running"}

# 유저 서비스 라우터 추가
app.include_router(auth_router, prefix="/api", tags=["auth"])