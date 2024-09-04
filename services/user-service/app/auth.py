from fastapi import APIRouter, HTTPException, status
from app.models import UserCreate, UserLogin
from app.utils import hash_password, verify_password, create_access_token
from datetime import timedelta

router = APIRouter()

# 간단한 가짜 데이터베이스
fake_users_db = {}

# 회원가입
@router.post("/signup", status_code=status.HTTP_201_CREATED)
def signup(user: UserCreate):
    if user.email in fake_users_db:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = hash_password(user.password)
    fake_users_db[user.email] = {"email": user.email, "username": user.username, "password": hashed_password}
    return {"msg": "User created successfully"}

# 로그인
@router.post("/login")
def login(user: UserLogin):
    db_user = fake_users_db.get(user.email)
    if not db_user or not verify_password(user.password, db_user["password"]):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    
    # JWT 토큰 발급
    access_token = create_access_token(data={"sub": user.email}, expires_delta=timedelta(minutes=30))
    return {"access_token": access_token, "token_type": "bearer"}