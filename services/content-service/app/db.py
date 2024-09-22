import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

# .env 파일에서 환경 변수 불러오기
load_dotenv()

# DATABASE_URL 환경 변수를 가져옴
DATABASE_URL = os.getenv("DATABASE_URL")

# 데이터베이스 엔진 및 세션 구성
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# 데이터베이스 세션 생성 함수
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
