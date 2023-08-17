"""src/user/base_config.py"""

from fastapi import Request
from fastapi_users import FastAPIUsers
from fastapi_users.authentication import (
    AuthenticationBackend,
    CookieTransport,
    JWTStrategy,
)

from src.config import AUTH_SECRET
from src.user.manager import get_user_manager
from src.user.models import User

cookie_transport = CookieTransport(cookie_max_age=3600)


def get_jwt_strategy() -> JWTStrategy:
    """Function that returns the JWTStrategy class"""
    return JWTStrategy(secret=AUTH_SECRET, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)


fastapi_users = FastAPIUsers[User, int](get_user_manager, [auth_backend])


async def get_enabled_backends(request: Request):
    """Return the enabled dependencies following custom logic."""
    return [auth_backend]


current_user = fastapi_users.current_user()
current_active_user = fastapi_users.current_user(
    active=True, get_enabled_backends=get_enabled_backends
)
