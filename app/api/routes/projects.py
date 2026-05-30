from typing import Annotated

from fastapi import APIRouter, HTTPException, Path, status

from app.api.deps import DbSession
from app.crud.projects import create_project, get_project
from app.crud.users import get_user
from app.schemas.project import ProjectCreate, ProjectRead

router = APIRouter(prefix="/projects", tags=["Projects"])


@router.post(
    "",
    response_model=ProjectRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create a project",
    description="Create a project.",
)
async def create_project_endpoint(project_data: ProjectCreate, session: DbSession) -> ProjectRead:
    if await get_user(session, project_data.owner_id) is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found.",
        )
    return await create_project(session, project_data)


@router.get(
    "/{id}",
    response_model=ProjectRead,
    summary="Get a project",
    description="Get a project by ID.",
)
async def get_project_endpoint(
    id: Annotated[int, Path(gt=0, description="Project ID")],
    session: DbSession,
) -> ProjectRead:
    project = await get_project(session, id)
    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found.",
        )
    return project
