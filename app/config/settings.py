import datetime
import sys
from functools import lru_cache

from pydantic_settings import BaseSettings

from app.config.logging_config import JSON_LOGS, Rotator

LOG_PATH = "app/logs"


class Settings(BaseSettings):
    app_env: str = "local"
    app_name: str = "Test"

    # 데이터베이스 설정
    db_user: str
    db_password: str
    db_host: str
    db_database: str
    db_port: int

    # cool sms 설정
    sms_sender: str
    sms_api_key: str
    sms_api_secret: str

    class Config:
        env_file = ".env"


class DevelopSettings(Settings):
    class Config:
        env_file = "develop.env"


class StagingSettings(Settings):
    class Config:
        env_file = "staging.env"


class ProductionSettings(Settings):
    class Config:
        env_file = "production.env"


class ApplicationSettings:
    @staticmethod
    def load():
        """
        환경 설정에 따라 적절한 설정 클래스를 로드합니다.
        """
        app_env = Settings().app_env
        if app_env in ["dev", "develop"]:
            settings = DevelopSettings()
        elif app_env in ["stage", "staging"]:
            settings = StagingSettings()
        elif app_env in ["prod", "production"]:
            settings = ProductionSettings()
        else:
            settings = Settings()
        return settings

    @staticmethod
    def log_config():
        """
        로깅 설정을 구성합니다.
        """
        log_format = (
            "{time:YYYY-MM-DD HH:mm:ss.SSS} | <level>{level: <8}</level> | <magenta>{process}:"
            "{thread.name}</magenta> <cyan>[{name}:{function}:{line}]</cyan> <level>{message}</level>"
        )
        rotator = Rotator(
            size=1e8, at=datetime.time(0, 0, 0)
        )  # 100MB 또는 0시에 새로운 로그 파일 생성
        config = {
            "handlers": [
                # 콘솔
                dict(
                    sink=sys.stdout,
                    format=log_format,
                    level="DEBUG",
                    serialize=JSON_LOGS,
                    backtrace=False,
                    diagnose=False,
                ),
                # 파일
                dict(
                    sink=f"{LOG_PATH}/application.log",
                    format=log_format,
                    level="INFO",
                    serialize=JSON_LOGS,
                    rotation=rotator.should_rotate,
                    compression="tar.gz",
                    backtrace=False,
                    diagnose=False,
                ),
            ]
        }
        return config


@lru_cache()
def get_settings() -> Settings:
    return ApplicationSettings.load()
