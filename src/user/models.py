"""src/user/models.py"""

from datetime import datetime

from fastapi_users.db import SQLAlchemyBaseUserTable
from sqlalchemy import TIMESTAMP, Boolean, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base
from src.user.constants import Role


class User(SQLAlchemyBaseUserTable[int], Base):
    """Class used to create Users in DB"""

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    email: Mapped[str] = mapped_column(
        String(length=320), unique=True, index=True, nullable=False
    )
    hashed_password: Mapped[str] = mapped_column(
        String(length=1024), nullable=False
    )
    first_name: Mapped[str] = mapped_column(String(length=100), nullable=True)
    last_name: Mapped[str] = mapped_column(String(length=100), nullable=True)
    role: Mapped[str] = mapped_column(String(length=10), default=Role.USER)
    is_active: Mapped[bool] = mapped_column(
        Boolean, default=True, nullable=True
    )
    is_verified: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )
    is_superuser: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )
    created_at: Mapped[TIMESTAMP] = mapped_column(
        TIMESTAMP, default=datetime.utcnow
    )
