from fastapi import APIRouter, HTTPException, status
from app.models import UserCreate, UserLogin
from app.utils import hash_password, verify_password, create_access_token
from datetime import timedelta

router = APIRouter()

# 간단한 가짜 데이터베이스
fake_users_db = {}

# 예외 처리 함수
def raise_http_exception(status_code, detail):
    raise HTTPException(status_code=status_code, detail=detail)


# 회원가입
@router.post("/signup", status_code=status.HTTP_201_CREATED)
def signup(user: UserCreate):
    # 이미 등록된 이메일인지 확인
    if user.email in fake_users_db:
        raise_http_exception(status.HTTP_400_BAD_REQUEST, "이미 가입된 이메일입니다.")
    
    try:
        # 비밀번호 해시 처리
        hashed_password = hash_password(user.password)
        fake_users_db[user.email] = {
            "email": user.email,
            "username": user.username,
            "password": hashed_password
        }
    except KeyError:
        raise_http_exception(status.HTTP_500_INTERNAL_SERVER_ERROR, "회원 정보 저장 중 오류가 발생했습니다.")

    return {"msg": "회원가입이 완료되었습니다."}


# 로그인
@router.post("/login")
def login(user: UserLogin):
    try:
        db_user = fake_users_db.get(user.email)

        # 이메일 또는 비밀번호가 잘못된 경우
        if not db_user or not verify_password(user.password, db_user["password"]):
            raise_http_exception(status.HTTP_400_BAD_REQUEST, "이메일 또는 비밀번호가 잘못되었습니다.")
        
        # JWT 토큰 발급
        access_token = create_access_token(data={"sub": user.email}, expires_delta=timedelta(minutes=30))

    except KeyError:
        raise_http_exception(status.HTTP_500_INTERNAL_SERVER_ERROR, "사용자 인증 중 오류가 발생했습니다.")
    
    return {"access_token": access_token, "token_type": "bearer"}
