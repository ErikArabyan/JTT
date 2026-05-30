from datetime import datetime

from pydantic import ConfigDict, Field, field_validator
from sqlmodel import SQLModel


class ProjectBase(SQLModel):
    name: str = Field(min_length=1, max_length=160, examples=["API Rewrite"])
    description: str | None = Field(default=None, examples=["Modernize the internal API."])

    @field_validator("name", mode="after")
    @classmethod
    def normalize_name(cls, name: str) -> str:
        name = name.strip()
        if not name:
            raise ValueError("Name must not be blank.")
        return name

    @field_validator("description", mode="after")
    @classmethod
    def normalize_description(cls, description: str | None) -> str | None:
        if description is None:
            return None
        description = description.strip()
        return description or None


class ProjectCreate(ProjectBase):
    owner_id: int = Field(gt=0, examples=[1])


class ProjectRead(ProjectBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    owner_id: int
    created_at: datetime
