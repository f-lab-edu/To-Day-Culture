# 베이스 이미지 선택 (Python 3.10)
FROM python:3.10

# 작업 디렉토리 설정
WORKDIR /app

# 필요 패키지 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 소스 코드 복사
COPY . .

# Alembic 마이그레이션 실행 후 Pytest만 실행, 앱 실행은 주석 처리
CMD alembic upgrade head && pytest
# CMD uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload  # 앱 실행 (필요 시 수동 실행)
