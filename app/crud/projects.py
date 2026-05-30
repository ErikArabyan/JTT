from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.project import Project
from app.schemas.project import ProjectCreate


async def create_project(session: AsyncSession, project_data: ProjectCreate) -> Project:
    project = Project(**project_data.model_dump())
    session.add(project)
    await session.commit()
    await session.refresh(project)
    return project


async def get_project(session: AsyncSession, project_id: int) -> Project | None:
    return await session.get(Project, project_id)


async def get_projects_for_user(session: AsyncSession, user_id: int) -> list[Project]:
    result = await session.exec(
        select(Project).where(Project.owner_id == user_id).order_by(Project.id)
    )
    return list(result.all())
