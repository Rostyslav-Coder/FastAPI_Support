"""src/user/routers.py"""

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import APIKeyHeader
from sqlalchemy.ext.asyncio import AsyncSession

from src.config import AUTH_SECRET
from src.database import get_async_session
from src.user.base_config import current_user
from src.user.constants import Role
from src.user.models import User

api_key_header = APIKeyHeader(name="X-API-KEY", auto_error=False)

router = APIRouter()


@router.put("/user-role")
async def update_user_role(
    secret: str,
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
):
    if secret != AUTH_SECRET:
        raise HTTPException(status_code=400, detail="Incorrect data")
    user.role = Role.MANAGER
    session.add(user)
    await session.commit()
    return {"message": "User role updated successfully"}
