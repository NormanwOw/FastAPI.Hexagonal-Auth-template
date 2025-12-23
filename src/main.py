import traceback
from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

from src.infrastructure.logger.logger import logger
from src.presentation.exceptions_mapper import exceptions_mapper
from src.presentation.routers.auth_router import router as auth_router
from src.presentation.routers.users_router import router as users_router


@asynccontextmanager
async def lifespan(_application: FastAPI) -> AsyncIterator[None]:
    logger.info('Start app...')
    yield
    logger.info('App shutdown')


app = FastAPI(
    title='{my_app} Service',
    version='0.0.1',
    docs_url='/docs',
    redoc_url=None,
    lifespan=lifespan,
)


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            response = await call_next(request)
            return response
        except tuple(exceptions_mapper.keys()) as ex:
            http_exc = exceptions_mapper[type(ex)]
            return JSONResponse(
                status_code=http_exc.status_code, content={'detail': http_exc.detail}
            )
        except Exception as exc:
            tb_str = ''.join(
                traceback.format_exception(type(exc), exc, exc.__traceback__)
            )
            logger.error(f'Exception during request: {exc}\nTraceback:\n{tb_str}')
            raise


app.add_middleware(LoggingMiddleware)
app.include_router(auth_router)
app.include_router(users_router)
