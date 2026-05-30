from datetime import datetime

from pydantic import ConfigDict, EmailStr, Field, field_validator
from sqlmodel import SQLModel


class UserBase(SQLModel):
    name: str = Field(min_length=1, max_length=120, examples=["Ada Lovelace"])
    email: EmailStr = Field(examples=["ada@example.com"])

    @field_validator("name", mode="after")
    @classmethod
    def normalize_name(cls, name: str) -> str:
        name = name.strip()
        if not name:
            raise ValueError("Name must not be blank.")
        return name

    @field_validator("email", mode="after")
    @classmethod
    def normalize_email(cls, email: EmailStr) -> str:
        return str(email).lower()


class UserCreate(UserBase):
    pass


class UserRead(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
