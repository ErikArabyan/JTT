from contextlib import asynccontextmanager
from collections.abc import AsyncGenerator

from fastapi import FastAPI

from app.api.routes.projects import router as projects_router
from app.api.routes.users import router as users_router
from app.db.session import create_database_schema
import app.models  # noqa: F401


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    await create_database_schema()
    yield


app = FastAPI(
    title="Mini User & Project Management API",
    summary="Create users and assign projects to them.",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(users_router)
app.include_router(projects_router)
