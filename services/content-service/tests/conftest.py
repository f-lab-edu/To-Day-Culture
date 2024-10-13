import sys
import os
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db import Base, get_test_db
from fastapi.testclient import TestClient
from app.main import app

# 프로젝트의 루트 경로를 PYTHONPATH에 추가
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

# 테스트용 데이터베이스 설정
TEST_DATABASE_URL = "postgresql://admin:1234@content-db:5432/test_content_db"
test_engine = create_engine(TEST_DATABASE_URL)
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

# pytest fixture: 테스트가 실행되기 전에 DB를 초기화하고, 테스트가 끝나면 데이터를 정리
@pytest.fixture(scope="module")
def test_db():
    Base.metadata.create_all(bind=test_engine)  # 테이블 생성
    yield TestSessionLocal()  # 테스트 실행
    Base.metadata.drop_all(bind=test_engine)  # 테스트가 끝나면 테이블 제거

@pytest.fixture(scope="module")
def client(test_db):
    # 테스트용 DB로 연결되도록 의존성을 덮어씌우기
    def _get_test_db_override():
        try:
            yield test_db
        finally:
            test_db.close()

    app.dependency_overrides[get_test_db] = _get_test_db_override
    with TestClient(app) as c:
        yield c
