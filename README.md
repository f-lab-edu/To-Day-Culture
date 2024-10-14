# To-day Culture

To-day Culture는 현대인의 문화생활을 더 쉽고 즐겁게 만들어주는 웹 애플리케이션입니다. 사용자들은 최신 영화, 공연, 뮤지컬 등의 정보를 확인하고, 개인화된 추천을 받으며, 일정 기반 검색 및 필터링 기능을 통해 원하는 콘텐츠를 쉽게 찾을 수 있습니다.

## 🚀 프로젝트 개요

이 프로젝트는 FastAPI를 사용하여 고성능 웹 API를 개발하고, 이를 통해 사용자들이 최신 문화 콘텐츠에 쉽게 접근할 수 있도록 합니다. RESTful API와 비동기 I/O를 활용하여 빠르고 효율적인 데이터 처리를 구현하였으며, 확장 가능하고 유지보수하기 쉬운 아키텍처를 목표로 설계되었습니다.

## 🛠 기술 스택

- **백엔드 프레임워크**: FastAPI
- **데이터베이스**: PostgreSQL (개발 및 테스트에서는 SQLite 사용)
- **ORM**: SQLAlchemy
- **인증**: JWT (JSON Web Tokens)
- **배포 및 인프라**: 네이버 클라우드 플랫폼 (NCP) (VPC, Auto Scaling, RDS, Object Storage)
- **API 문서화**: 자동 OpenAPI 생성 (Swagger UI)
- **CI/CD**: GitHub Actions
- **기타 도구**: Docker, Alembic (DB 마이그레이션), Pytest (테스트)

## ERD
![Untitled (3)](https://github.com/user-attachments/assets/d03feea0-2087-4cdc-9d7f-886405081344)

## 🔖 Infra structure
![cloud ar drawio](https://github.com/user-attachments/assets/e620a26c-0996-43ec-948f-49603fe90c24)


# To-day-Art Project Structure

```bash
To-day-Art/
├── api-gateway/                    # NGINX 또는 API Gateway 설정을 위한 디렉토리
│   └── nginx.conf                  # NGINX API Gateway 설정 파일
├── services/
│   ├── user-service/               # 사용자 관련 기능을 담당하는 서비스
│   │   ├── app/                    # FastAPI 애플리케이션 디렉토리
│   │   │   ├── main.py             # FastAPI 진입점, 라우터 등록 및 서버 실행
│   │   │   ├── auth.py             # 인증/회원가입/로그인 관련 로직
│   │   │   ├── models.py           # 데이터베이스 모델 및 Pydantic 스키마 정의
│   │   │   ├── routers/            # 다양한 라우터가 들어가는 디렉토리
│   │   │   └── services/           # 비즈니스 로직 및 서비스 기능 정의
│   │   ├── tests/                  # 단위 테스트 및 통합 테스트 디렉토리
│   │   │   ├── test_auth.py        # 인증 관련 테스트 파일
│   │   ├── requirements.txt        # 필요한 패키지 목록
│   │   ├── Dockerfile              # Docker 이미지 생성을 위한 파일
│   │   └── .env                    # 환경 변수 파일 (DB 정보 및 SECRET_KEY)
│   ├── content-service/            # 문화 콘텐츠 관련 정보를 제공하는 서비스
│   │   ├── app/
│   │   │   ├── main.py
│   │   │   ├── routers/            # 영화, 공연, 뮤지컬 등 콘텐츠 라우터
│   │   └── requirements.txt        # 필요한 패키지 목록
│   ├── review-service/             # 리뷰 작성 및 관리 서비스
│   │   ├── app/
│   │   │   ├── main.py
│   │   │   ├── routers/            # 리뷰 관련 라우터
│   │   └── requirements.txt        # 필요한 패키지 목록
├── shared/                         # 여러 서비스에서 공통으로 사용하는 유틸리티
│   ├── db.py                       # 데이터베이스 연결 및 세션 관리 코드
│   ├── utils.py                    # 공통 유틸리티 함수들
├── docker-compose.yml              # 전체 프로젝트 Docker 설정
├── .env                            # 공통 환경 변수 파일
└── README.md                       # 프로젝트 개요 및 설명
```


## 📚 유즈케이스

### 1. 사용자 인증 및 관리
- **회원가입**: 사용자는 이메일과 비밀번호를 통해 계정을 생성할 수 있습니다.
- **로그인**: JWT를 활용한 토큰 기반 인증을 통해 사용자가 안전하게 로그인할 수 있습니다.
- **로그아웃**: 클라이언트에서 토큰을 제거하는 방식으로 로그아웃을 처리합니다.

### 2. 콘텐츠 정보 제공
- **콘텐츠 등록 및 조회**: 영화, 공연, 뮤지컬 등의 정보를 제공하며, 사용자는 이를 조회할 수 있습니다.
- **일정 기반 검색**: 사용자가 특정 기간 내에 제공되는 콘텐츠를 검색하고 필터링할 수 있습니다.
- **리뷰 및 평점**: 사용자는 콘텐츠에 대한 리뷰와 평점을 남길 수 있으며, 다른 사용자의 평가를 확인할 수 있습니다.

### 3. 개인화된 경험
- **추천 시스템**: 사용자의 선호도를 기반으로 개인화된 콘텐츠 추천을 제공합니다.
- **알림 기능**: 사용자가 관심 있는 콘텐츠의 업데이트 및 일정 변경 사항을 알림으로 받을 수 있습니다.

## 🛤 개발 방향성

1. **확장 가능한 아키텍처**:
   - 마이크로서비스 아키텍처를 고려한 설계로, 각 기능이 독립적으로 확장될 수 있도록 합니다.
   - 모듈화된 코드 구조를 통해 유지보수성과 테스트 용이성을 높였습니다.

2. **고성능 비동기 처리**:
   - FastAPI의 비동기 I/O 기능을 적극 활용하여 대규모 트래픽 처리에도 효율적인 시스템을 구축합니다.
   - PostgreSQL과 Redis를 연계하여 빠른 데이터 접근 및 캐싱 전략을 적용합니다.

3. **자동화된 배포 및 테스트**:
   - CI/CD 파이프라인을 구축하여 코드 변경 사항이 자동으로 테스트되고 배포되도록 하였습니다.
   - Docker 컨테이너화를 통해 일관된 개발 및 운영 환경을 유지합니다.

4. **보안 강화**:
   - JWT 기반 인증을 사용하여 안전한 사용자 인증을 보장합니다.
   - 네이버 클라우드 플랫폼의 VPC 및 IAM 설정을 통해 클라우드 환경에서의 보안을 강화합니다.
<br>


## 🥊 주요 개발 이슈 및 해결방안

**[[Fastapi 서비스 구조 선정]](https://www.notion.so/fastapi-06cbe46705d44e25a3115550e143a5f8)**
<br>
<br>
**[[Fastapi 이메일 회원가입 유효성 검증 테스트 케이스 오류]](https://www.notion.so/82368a9e110943929208267f6f346ee8)**
<br>
<br>
**[[콘텐츠 조회 모델 인덱스 쿼리 최적화]](https://www.notion.so/82368a9e110943929208267f6f346ee8)**
<br>
<br>
**[[콘텐츠 조회 쿼리 최적화]](https://www.notion.so/1123c1810b61804086aae14e81367892)**
<br>
<br>
**[[k6 데이터 조회 부하 테스트]](https://www.notion.so/K6-1-11f3c1810b6180b79805c44f279f723c)**
<br>
<br>

