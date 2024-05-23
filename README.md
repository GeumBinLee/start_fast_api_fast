
코드 복사
# Project Structure

## Directory Layout

```plaintext
.
├── README.md
├── __pycache__
│   ├── database.cpython-311.pyc
│   └── main.cpython-311.pyc
├── app
│   ├── __init__.py
│   ├── __pycache__
│   │   └── __init__.cpython-311.pyc
│   ├── config
│   │   ├── __init__.py
│   │   ├── __pycache__
│   │   │   ├── __init__.cpython-311.pyc
│   │   │   ├── database.cpython-311.pyc
│   │   │   ├── logging_config.cpython-311.pyc
│   │   │   └── settings.cpython-311.pyc
│   │   ├── database.py
│   │   ├── logging_config.py
│   │   └── settings.py
│   ├── constants
│   │   └── __init__.py
│   ├── controllers
│   │   ├── __init__.py
│   │   └── endpoints
│   │       └── __init__.py
│   ├── core
│   │   ├── __init__.py
│   │   ├── __pycache__
│   │   │   ├── __init__.cpython-311.pyc
│   │   │   ├── enums.cpython-311.pyc
│   │   │   ├── environment.cpython-311.pyc
│   │   │   ├── exceptions.cpython-311.pyc
│   │   │   ├── localization.cpython-311.pyc
│   │   │   ├── request_utils.cpython-311.pyc
│   │   │   └── scheduler.cpython-311.pyc
│   │   ├── enums.py
│   │   ├── environment.py
│   │   ├── exceptions.py
│   │   ├── localization.py
│   │   ├── request_utils.py
│   │   └── scheduler.py
│   ├── dto
│   │   └── __init__.py
│   ├── logs
│   │   └── application.log
│   ├── middlewares
│   │   └── __init__.py
│   ├── schemas
│   │   └── __init__.py
│   └── services
│       ├── __init__.py
│       ├── __pycache__
│       │   ├── __init__.cpython-311.pyc
│       │   ├── measure_time.cpython-311.pyc
│       │   ├── request_api.cpython-311.pyc
│       │   └── sms_service.cpython-311.pyc
│       ├── measure_time.py
│       ├── request_api.py
│       └── sms_service.py
├── logs
│   ├── __init__.py
│   └── application.log
├── main.py
├── resources
│   ├── languages
│   │   ├── en.json
│   │   └── ko.json
│   └── static
└── tests
    └── __init__.py
```
## File Descriptions
### main.py
- FastAPI 애플리케이션을 초기화하고 구성하는 메인 파일입니다.
### app/config
- database.py: 데이터베이스 연결 및 쿼리 실행 로직을 포함합니다.
- logging_config.py: 로깅 설정을 포함합니다.
- settings.py: 환경 설정을 포함합니다.
### app/constants
- 프로젝트의 상수를 정의합니다.
### app/controllers
- API 엔드포인트를 정의합니다.
### app/core
- enums.py: 열거형(Enum) 클래스를 포함합니다.
- environment.py: 환경 관련 열거형을 정의합니다.
- exceptions.py: 커스텀 예외 클래스를 정의합니다.
- localization.py: 다국어 지원을 위한 로직을 포함합니다.
- request_utils.py: 요청 관련 유틸리티 함수를 포함합니다.
- scheduler.py: 스케줄러 관련 로직을 포함합니다.
### app/dto
- 데이터 전송 객체를 정의합니다.
### app/logs
- 로그 파일을 저장합니다.
### app/middlewares
- 미들웨어 관련 코드를 포함합니다.
### app/schemas
- 데이터 유효성 검사 및 직렬화를 위한 Pydantic 모델을 정의합니다.
### app/services
- 비즈니스 로직 및 서비스 관련 코드를 포함합니다.
- measure_time.py: 함수 실행 시간을 측정하는 유틸리티를 포함합니다.
- request_api.py: 외부 API 요청을 처리하는 유틸리티를 포함합니다.
- sms_service.py: SMS 전송 서비스를 포함합니다.
### resources
- 애플리케이션에서 사용하는 정적 자원들을 포함합니다.
- languages: 다국어 지원을 위한 언어 파일을 포함합니다.
- static: 정적 파일을 포함합니다.
### tests
- 테스트 코드를 포함합니다.
