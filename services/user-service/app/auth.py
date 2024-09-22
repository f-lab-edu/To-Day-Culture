from sqlalchemy.orm import Session
from fastapi import Depends, APIRouter, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.models import User
from app.db import get_db
from app.schemas import UserCreate, UserLogin
from app.utils import hash_password, verify_password, create_access_token, verify_access_token
from datetime import timedelta

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# 회원가입
@router.post("/signup", status_code=201)
def signup(user: UserCreate, db: Session = Depends(get_db)):
    # 중복 이메일 체크
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        print("이미 가입된 이메일:", user.email)
        raise HTTPException(status_code=400, detail="이미 가입된 이메일입니다.")
    
    # 유저 생성
    hashed_password = hash_password(user.password)
    new_user = User(email=user.email, username=user.username, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"msg": "회원가입이 완료되었습니다."}

# 로그인
@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="이메일 또는 비밀번호가 잘못되었습니다.")

    # JWT 토큰 발급
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(data={"sub": user.email}, expires_delta=access_token_expires)
    
    return {"access_token": access_token, "token_type": "bearer"}

# 보호된 엔드포인트
@router.get("/protected-endpoint")
def protected_route(token: str = Depends(oauth2_scheme)):
    try:
        email = verify_access_token(token)
        return {"msg": f"안녕하세요, {email}님! 이곳은 보호된 엔드포인트입니다."}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="유효하지 않은 인증 자격 증명입니다.")
