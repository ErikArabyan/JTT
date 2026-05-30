from datetime import UTC, datetime
from typing import TYPE_CHECKING

from sqlalchemy import Column, DateTime, ForeignKey, Index, Integer, String, Text
from sqlmodel import Field, Relationship, SQLModel


if TYPE_CHECKING:
    from app.models.user import User


class Project(SQLModel, table=True):
    __tablename__ = "projects"
    __table_args__ = (Index("ix_projects_owner_id", "owner_id"),)

    id: int | None = Field(default=None, primary_key=True, index=True)
    name: str = Field(sa_column=Column(String(160), nullable=False))
    description: str | None = Field(
        default=None,
        sa_column=Column(Text, nullable=True),
    )
    owner_id: int = Field(
        sa_column=Column(
            Integer,
            ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
        )
    )
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        sa_column=Column(
            DateTime(timezone=True),
            nullable=False,
        ),
    )

    owner: "User" = Relationship(back_populates="projects")
