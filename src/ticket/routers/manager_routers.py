"""src/ticket/routers/manager_routers.py"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.ticket.constants import TicketStatus
from src.ticket.models import Ticket
from src.ticket.schemas import TicketOut
from src.user.base_config import current_user
from src.user.constants import Role
from src.user.schemas import UserRead

router = APIRouter()


@router.get("/all", response_model=list[TicketOut])
async def ticket_get_all(
    user: UserRead = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
):
    if user.role != str(Role.MANAGER):
        raise HTTPException(status_code=403, detail="Forbidden")

    query = select(Ticket).where(Ticket.manager_id.is_(None))
    result = await session.execute(query)
    tickets = result.scalars().all()
    return tickets


@router.patch("/asign", response_model=TicketOut)
async def ticket_asign(
    ticket_id: int,
    user: UserRead = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
):
    if user.role != str(Role.MANAGER):
        raise HTTPException(status_code=403, detail="Forbidden")

    query = select(Ticket).where(Ticket.id == ticket_id)
    result = await session.execute(query)
    ticket = result.scalar_one_or_none()

    if ticket is None:
        raise HTTPException(status_code=204)

    ticket.manager_id = user.id
    ticket.status = TicketStatus.IN_PROGRESS
    session.add(ticket)
    await session.commit()
    await session.refresh(ticket)
    return ticket
