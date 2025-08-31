from fastapi import FastAPI

from src.api.main_router import main_router
from src.core.config import settings

app = FastAPI(
    title=settings.TITLE,
    version=settings.VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
)

app.include_router(main_router)
