"""src/ticket/routers.py"""

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


@router.post("/create", response_model=TicketOut)
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
    if user.role == str(Role.USER):
        query = select(Ticket).where(Ticket.user_id == user.id)

    elif user.role == str(Role.MANAGER):
        query = select(Ticket).where(
            and_(
                Ticket.manager_id == user.id,
                Ticket.status != str(TicketStatus.CLOSED),
            )
        )

    result = await session.execute(query)
    tickets = result.scalars().all()
    return tickets


@router.get("/free", response_model=list[TicketOut])
async def ticket_get_free(
    user: UserRead = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
):
    if user.role != str(Role.MANAGER):
        raise HTTPException(status_code=403, detail="Forbidden")

    query = select(Ticket).where(Ticket.manager_id.is_(None))
    result = await session.execute(query)
    ticket = result.scalars().all()
    return ticket


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


@router.patch("/close", response_model=TicketOut)
async def ticket_close(
    ticket_id: int,
    user: UserRead = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
):
    if user.role != str(Role.MANAGER):
        raise HTTPException(status_code=403, detail="Forbidden")

    query = select(Ticket).where(Ticket.id == ticket_id)
    result = await session.execute(query)
    ticket = result.scalar_one_or_none()
    ticket.status = TicketStatus.CLOSED
    session.add(ticket)
    await session.commit()
    await session.refresh(ticket)
    return ticket


@router.get("/all_closed", response_model=list[TicketOut])
async def ticket_get_all_my_closed(
    user: UserRead = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
):
    if user.role != str(Role.MANAGER):
        raise HTTPException(status_code=403, detail="Forbidden")

    query = select(Ticket).where(
        and_(
            Ticket.manager_id == user.id,
            Ticket.status == str(TicketStatus.CLOSED),
        )
    )
    result = await session.execute(query)
    tickets = result.scalars().all()
    return tickets
