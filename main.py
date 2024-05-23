import logging
import sys
from fastapi import APIRouter, FastAPI, HTTPException, Request
from fastapi.exceptions import (
    HTTPException as StarletteHTTPException,
    RequestValidationError,
)
from fastapi.responses import JSONResponse
from loguru import logger
from starlette.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from config.database import execute_query
from config.log_config import InterceptHandler
from config.setting import ApplicationSettings
from core.common import scheduler
from core.common.custom_exception import ReturnHandler

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
    # 시작 시 실행할 코드
    await server_on()
    yield
    # 종료 시 실행할 코드
    pass

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
    return {"message": "테스트 화면"}


@app.get("/items/{item_id}")
def read_item(item_id: int):
    return {"message": f"item_id로 {item_id} 받음"}
    # try:
    #     test_query = "SELECT * FROM items WHERE id = %s"
    #     item = execute_query(test_query, method="fetchone")
    #     if item:
    #         return {"message": item}
    #     else:
    #         raise HTTPException(status_code=404, detail="아이템 없음")
    # except Exception as e:
    #     raise HTTPException(status_code=500, detail=str(e))


async def server_on():
    pass


@app.middleware("http")
async def log_request(request: Request, call_next):
    response = await call_next(request)
    client_host, client_port = request.client
    full_request = f'{client_host}:{client_port} - "{request.method} {request.url.path}?{request.query_params}" {response.status_code}'
    logger.info(full_request)
    return response


@app.exception_handler(ReturnHandler)
async def database_exception_handler(request: Request, exc: ReturnHandler):
    return JSONResponse(
        status_code=exc.status_code,
        content={"result": "FAILED", "message": exc.message},
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={"result": "FAILED", "message": str(exc)},
    )


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"result": "FAILED", "message": str(exc.detail)},
    )


@app.exception_handler(Exception)
async def all_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"result": "FAILED", "message": str(exc)},
    )
