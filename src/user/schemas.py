"""src/user/schemas.py"""

from datetime import datetime
from typing import Optional

from fastapi_users.schemas import BaseUser, BaseUserCreate, BaseUserUpdate
from pydantic import ConfigDict, EmailStr, validator

from src.user.constants import Role


class UserRead(BaseUser[int]):
    """User Data Output Model"""

    id: int
    email: str
    first_name: Optional[str]
    last_name: Optional[str]
    role: Role
    created_at: datetime

    __config__ = ConfigDict(from_attributes=True)


class UserCreate(BaseUserCreate):
    """User Data Input Model"""

    email: EmailStr
    password: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None

    @validator("password")
    def validate_password(cls, password):  # pylint: disable=E0213
        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters long")
        if not any(c.isupper() for c in password):
            raise ValueError(
                "Password must contain at least one uppercase letter"
            )
        if not any(c.islower() for c in password):
            raise ValueError(
                "Password must contain at least one lowercase letter"
            )
        if not any(c.isdigit() for c in password):
            raise ValueError("Password must contain at least one digit")
        return password


class UserUpdate(BaseUserUpdate):
    """User Data Input Model"""

    first_name: Optional[str] = None
    last_name: Optional[str] = None
