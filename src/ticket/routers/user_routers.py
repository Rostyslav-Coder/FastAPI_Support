"""src/ticket/routers/user_routers.py"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.ticket.constants import TicketStatus
from src.ticket.models import Ticket
from src.ticket.schemas import TicketIn, TicketOut
from src.user.base_config import current_user
from src.user.constants import Role
from src.user.schemas import UserRead

router = APIRouter()


@router.post("/", response_model=TicketOut)
async def ticket_create(
    ticket: TicketIn,
    user: UserRead = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
):
    if user.role != str(Role.USER):
        raise HTTPException(status_code=403, detail="Forbidden")

    result = Ticket(
        title=ticket.title,
        text=ticket.text,
        user_id=user.id,
        status=TicketStatus.NOT_STARTED,
    )
    session.add(result)
    await session.commit()
    await session.refresh(result)
    return result


@router.get("/all", response_model=list[TicketOut])
async def ticket_get_all(
    user: UserRead = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
):
    if user.role != str(Role.USER):
        raise HTTPException(status_code=403, detail="Forbidden")

    query = select(Ticket).where(Ticket.user_id == user.id)
    result = await session.execute(query)
    tickets = result.scalars().all()
    return tickets


@router.get("/ticket_id/{id}", response_model=TicketOut)
async def ticket_get_by_id(
    ticket_id: int,
    user: UserRead = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
):
    if user.role != str(Role.USER):
        raise HTTPException(status_code=403, detail="Forbidden")

    query = select(Ticket).where(
        and_(Ticket.user_id == user.id, Ticket.id == ticket_id)
    )
    result = await session.execute(query)
    ticket = result.scalar_one_or_none()
    return ticket


@router.get("/ticket_title/{title}", response_model=list[TicketOut])
async def ticket_get_by_title(
    ticket_title: str,
    user: UserRead = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
):
    if user.role != str(Role.USER):
        raise HTTPException(status_code=403, detail="Forbidden")

    query = select(Ticket).where(
        and_(Ticket.user_id == user.id, Ticket.title == ticket_title)
    )
    result = await session.execute(query)
    ticket = result.scalars().all()
    return ticket
