import sentry_sdk
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from app.api.api_v1.api import api_router
from app.llms.api.routes import routers
from app.core.config import settings

sentry_sdk.init(
    dsn=settings.SENTRY_DSN,
    traces_sample_rate=1.0,
)


app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f'{settings.API_V1_STR}/openapi.json',
    debug=False if settings.ENVIRONMENT == 'prod' else True,
    docs_url="/documents" if settings.ENVIRONMENT == 'prod' else '/docs',
    redoc_url=None if settings.ENVIRONMENT == 'prod' else '/redoc',
)


app.include_router(api_router, prefix=settings.API_V1_STR)
app.include_router(routers, prefix=settings.API_V1_STR)
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)
app.add_middleware(SessionMiddleware, secret_key="some-random-string", max_age=None)


@app.get('/health', tags=['health-check'])
async def health():
    return {'message': 'ok!'}
