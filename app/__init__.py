# 패키지 초기화 시 필요한 설정 또는 모듈 임포트
from .config import database, logging_config, settings
from .core import (enums, environment, exceptions, localization, request_utils,
                   scheduler)
from .services import measure_time, request_api, sms_service

# 패키지 초기화 코드
print("App 패키지가 초기화되었습니다.")
