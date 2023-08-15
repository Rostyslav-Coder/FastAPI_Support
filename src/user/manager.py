"""src/manager.py"""

from typing import Optional

from fastapi import Depends, Request
from fastapi_users import (
    BaseUserManager,
    IntegerIDMixin,
    exceptions,
    models,
    schemas,
)

from src.config import MANAGER_SECRET
from src.user.constants import Role
from src.user.models import User
from src.user.utils import get_user_db


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    """User to manage Users"""

    reset_password_token_secret = MANAGER_SECRET
    verification_token_secret = MANAGER_SECRET

    async def on_after_register(
        self, user: User, request: Optional[Request] = None
    ):
        print(f"User {user.id} has registered.")

    async def on_after_request_verify(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        print(
            f"Verification requested for user {user.id}. Verification token: {token}"
        )

    async def create(
        self,
        user_create: schemas.UC,
        safe: bool = False,
        request: Optional[Request] = None,
    ) -> models.UP:
        await self.validate_password(user_create.password, user_create)

        existing_user = await self.user_db.get_by_email(user_create.email)
        if existing_user is not None:
            raise exceptions.UserAlreadyExists()

        user_dict = (
            user_create.create_update_dict()
            if safe
            else user_create.create_update_dict_superuser()
        )
        password = user_dict.pop("password")
        user_dict["hashed_password"] = self.password_helper.hash(password)
        user_dict["role"] = Role.USER

        created_user = await self.user_db.create(user_dict)

        await self.on_after_register(created_user, request)

        return created_user


async def get_user_manager(
    user_db=Depends(get_user_db),
):
    """Function to Create User`s managment"""
    yield UserManager(user_db)
