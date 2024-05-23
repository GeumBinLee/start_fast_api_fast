import logging
import sys
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import HTTPException as StarletteHTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from loguru import logger
from starlette.middleware.cors import CORSMiddleware

from app.config.database import execute_query
from app.config.logging_config import InterceptHandler
from app.config.settings import ApplicationSettings
from app.core import scheduler
from app.core.exceptions import ReturnHandler
from app.core.localization import load_languages

# 로그 설정 (Loguru)
logging.root.handlers = [InterceptHandler()]
logging.root.setLevel(logging.DEBUG)

for name in logging.root.manager.loggerDict.keys():
    logging.getLogger(name).handlers = []
    logging.getLogger(name).propagate = True

logger.configure(**ApplicationSettings.log_config())

# 스케줄러 실행
scheduler.start()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    애플리케이션의 수명 주기 이벤트를 처리합니다.
    """
    await server_on()
    yield


app = FastAPI(
    title="카카오 알림톡",
    redoc_url=None,
    debug=True,
    docs_url="/docs",
    lifespan=lifespan,
)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    """
    루트 엔드포인트로, 테스트 메시지를 반환합니다.
    """
    return {"message": "테스트 화면"}


@app.get("/items/{item_id}")
def read_item(item_id: int):
    """
    아이템 ID를 받아서 메시지를 반환합니다.
    """
    return {"message": f"item_id로 {item_id} 받음"}


async def server_on():
    """
    애플리케이션 시작 시 실행할 작업을 정의합니다.
    """
    load_languages()


@app.middleware("http")
async def log_request(request: Request, call_next):
    """
    모든 HTTP 요청을 로깅하는 미들웨어입니다.
    """
    response = await call_next(request)
    client_host, client_port = request.client
    full_request = f'{client_host}:{client_port} - "{request.method} {request.url.path}?{request.query_params}" {response.status_code}'
    logger.info(full_request)
    return response


@app.exception_handler(ReturnHandler)
async def database_exception_handler(request: Request, exc: ReturnHandler):
    """
    데이터베이스 예외를 처리하는 핸들러입니다.
    """
    return JSONResponse(
        status_code=exc.status_code,
        content={"result": "FAILED", "message": exc.message},
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    요청 유효성 검사 예외를 처리하는 핸들러입니다.
    """
    return JSONResponse(
        status_code=422,
        content={"result": "FAILED", "message": str(exc)},
    )


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    """
    HTTP 예외를 처리하는 핸들러입니다.
    """
    return JSONResponse(
        status_code=exc.status_code,
        content={"result": "FAILED", "message": str(exc.detail)},
    )


@app.exception_handler(Exception)
async def all_exception_handler(request: Request, exc: Exception):
    """
    모든 예외를 처리하는 핸들러입니다.
    """
    return JSONResponse(
        status_code=500,
        content={"result": "FAILED", "message": str(exc)},
    )
