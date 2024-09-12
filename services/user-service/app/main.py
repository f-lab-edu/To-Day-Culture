from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordBearer
from app.auth import router as auth_router
from starlette.responses import JSONResponse

# FastAPI 애플리케이션 생성
app = FastAPI()

# OAuth2PasswordBearer 설정 (JWT 토큰을 사용해 보호된 엔드포인트 인증)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# 회원가입 및 로그인 라우터 등록
app.include_router(auth_router, prefix="/auth")

# 보호된 엔드포인트 추가
@app.get("/protected-endpoint")
async def protected_route(token: str = Depends(oauth2_scheme)):
    # JWT 토큰을 검증한 후 필요한 작업을 수행
    return JSONResponse({"message": "This is a protected route"})