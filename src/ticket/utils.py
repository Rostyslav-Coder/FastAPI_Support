"""src/ticket/utils.py"""

from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.ticket.schemas import TicketOut
from src.user.base_config import current_user
from src.user.constants import Role


class RoleRequired:
    def __init__(self, role: Role):
        self.role = role

    async def __call__(self, user=Depends(current_user)):
        if user.role != str(self.role):
            raise HTTPException(status_code=403, detail="Forbidden")
        return user


async def add_and_commit(session: AsyncSession, result) -> TicketOut:
    session.add(result)
    await session.commit()
    await session.refresh(result)
    return result


async def execute_query_all(session: AsyncSession, query) -> TicketOut:
    result = await session.execute(query)
    tickets = result.scalars().all()

    return tickets


async def execute_query_one(session: AsyncSession, query) -> TicketOut:
    result = await session.execute(query)
    ticket = result.scalar_one_or_none()

    return ticket
