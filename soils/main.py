from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from soils.routes import api_router
from soils.config import settings
from soils.logs import setup_logLevels

setup_logLevels()


app = FastAPI(title=settings.PROJECT_NAME)

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(api_router, prefix=settings.API_V1_STR)
