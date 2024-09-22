from fastapi import FastAPI
from app.db import engine, Base

app = FastAPI()

# 테이블 자동 생성
Base.metadata.create_all(bind=engine)
