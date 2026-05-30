from typing import Annotated

from fastapi import Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from app.db.session import get_db_session

DbSession = Annotated[AsyncSession, Depends(get_db_session)]
