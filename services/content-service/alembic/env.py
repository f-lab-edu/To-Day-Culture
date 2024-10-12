import os
import sys
from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context
from dotenv import load_dotenv  # .env 파일에서 환경 변수를 불러오기 위해 추가

# .env 파일의 경로를 지정하고, 불러오기
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))  # .env 파일을 현재 디렉토리에서 상위로 설정

# 현재 디렉토리의 부모 디렉토리를 시스템 경로에 추가
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# models.py를 import하여 Base.metadata에 테이블 정보 등록
from app import models  # app 폴더에 models.py가 있는 경우
from app.db import Base  # 기존 프로젝트의 Base 객체 가져오기

# Alembic 설정 객체
config = context.config

# .env 파일에서 DATABASE_URL 환경 변수를 불러와 Alembic 설정에 추가
database_url = os.getenv("DATABASE_URL")
if database_url:
    config.set_main_option('sqlalchemy.url', database_url)

# 로깅 설정
fileConfig(config.config_file_name)

# target_metadata를 설정하여 Alembic이 모델의 메타데이터를 인식하도록 함
target_metadata = Base.metadata

# 'offline' 모드에서 마이그레이션 실행 함수
def run_migrations_offline():
    """Run migrations in 'offline' mode.
    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well. By skipping the Engine creation
    we don't even need a DBAPI to be available.
    Calls to context.execute() here emit the given string to the
    script output.
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

# 'online' 모드에서 마이그레이션 실행 함수
def run_migrations_online():
    """Run migrations in 'online' mode.
    In this scenario we need to create an Engine
    and associate a connection with the context.
    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

# Alembic이 'offline' 모드인지 'online' 모드인지에 따라 함수를 호출
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
