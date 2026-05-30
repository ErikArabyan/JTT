from typing import Annotated

from fastapi import APIRouter, HTTPException, Path, Query, Response, status
from sqlalchemy.exc import IntegrityError

from app.api.deps import DbSession
from app.crud.projects import get_projects_for_user
from app.crud.users import (
    create_user,
    delete_user,
    get_user,
    get_user_by_email,
    list_users,
)
from app.schemas.project import ProjectRead
from app.schemas.user import UserCreate, UserRead

router = APIRouter(prefix="/users", tags=["Users"])


@router.post(
    "",
    response_model=UserRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create a user",
    description="Create a user.",
)
async def create_user_endpoint(user_data: UserCreate, session: DbSession) -> UserRead:
    existing_user = await get_user_by_email(session, str(user_data.email))
    if existing_user is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A user with this email already exists.",
        )

    try:
        return await create_user(session, user_data)
    except IntegrityError as error:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Invalid request data.",
        ) from error


@router.get(
    "",
    response_model=list[UserRead],
    summary="User list",
    description="User list with pagination.",
)
async def list_users_endpoint(
    session: DbSession,
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
) -> list[UserRead]:
    return await list_users(session, limit=limit, offset=offset)


@router.get(
    "/{id}",
    response_model=UserRead,
    summary="Get a user",
    description="Get a user by id.",
)
async def get_user_endpoint(
    id: Annotated[int, Path(gt=0, description="User ID")],
    session: DbSession,
) -> UserRead:
    user = await get_user(session, id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found.",
        )
    return user


@router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a user",
    description="Delete a user and cascade-delete projects owned by that user.",
)
async def delete_user_endpoint(
    id: Annotated[int, Path(gt=0, description="User ID")],
    session: DbSession,
) -> Response:
    user = await get_user(session, id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found.",
        )

    await delete_user(session, user)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get(
    "/{id}/projects",
    response_model=list[ProjectRead],
    summary="List user projects",
    description="List all projects owned by a user.",
)
async def get_user_projects_endpoint(
    id: Annotated[int, Path(gt=0, description="User ID")],
    session: DbSession,
) -> list[ProjectRead]:
    if await get_user(session, id) is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found.",
        )
    return await get_projects_for_user(session, id)
