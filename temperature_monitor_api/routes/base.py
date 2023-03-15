import os

from fastapi import FastAPI
from fastapi import Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi_sqlalchemy import DBSessionMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse

from temperature_monitor_api import __version__
from temperature_monitor_api.settings import get_settings
from temperature_monitor_api.routes.measurements import router as measurements_router
from temperature_monitor_api.routes.devices import router as devices_router

settings = get_settings()

app = FastAPI(
    title='temperature-monitor-api',
    description='temperature-monitor-api',
    version=__version__,
    root_path='/',
    docs_url='/docs',
    redoc_url=None,
)

app.add_middleware(
    DBSessionMiddleware,
    db_url=settings.DB_DSN,
    engine_args={"pool_pre_ping": True, "isolation_level": "AUTOCOMMIT"},
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ALLOW_ORIGINS,
    allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
    allow_methods=settings.CORS_ALLOW_METHODS,
    allow_headers=settings.CORS_ALLOW_HEADERS,
)

app.include_router(measurements_router, prefix='', tags=['measurements'])
app.include_router(devices_router, prefix='', tags=['devices'])


# @app.get("/")
# def serve_home(request: Request):
#     return FileResponse("../../static/index.html")
#
#
# app.mount('/static', StaticFiles(directory='../../static', html=True), 'static')

parent_dir_path = os.path.dirname(os.path.realpath(__file__))
print('WORKDIR', parent_dir_path)
