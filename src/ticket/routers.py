"""src/ticket/routers.py"""

from fastapi import APIRouter, Depends
from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.ticket.constants import TicketStatus
from src.ticket.models import Message, Ticket
from src.ticket.schemas import MessageOut, TicketIn, TicketOut
from src.ticket.utils import (
    RoleRequired,
    add_and_commit,
    execute_query_all,
    execute_query_one,
)
from src.user.base_config import current_user
from src.user.constants import Role
from src.user.schemas import UserRead

router = APIRouter()


@router.post("/create", response_model=TicketOut)
async def ticket_create(
    ticket: TicketIn,
    user: UserRead = Depends(RoleRequired(Role.USER)),
    session: AsyncSession = Depends(get_async_session),
):
    result = Ticket(
        title=ticket.title,
        text=ticket.text,
        user_id=user.id,
        status=TicketStatus.NOT_STARTED,
    )

    result = await add_and_commit(session, result)

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

    tickets = await execute_query_all(session, query)

    return tickets


@router.get("/free", response_model=list[TicketOut])
async def ticket_get_free(
    user: UserRead = Depends(RoleRequired(Role.MANAGER)),
    session: AsyncSession = Depends(get_async_session),
):
    query = select(Ticket).where(Ticket.manager_id.is_(None))

    tickets = await execute_query_all(session, query)

    return tickets


@router.patch("/asign", response_model=TicketOut)
async def ticket_asign(
    ticket_id: int,
    user: UserRead = Depends(RoleRequired(Role.MANAGER)),
    session: AsyncSession = Depends(get_async_session),
):
    query = select(Ticket).where(Ticket.id == ticket_id)

    ticket = await execute_query_one(session, query)

    ticket.manager_id = user.id
    ticket.status = TicketStatus.IN_PROGRESS

    result = await add_and_commit(session, ticket)

    return result


@router.patch("/close", response_model=TicketOut)
async def ticket_close(
    ticket_id: int,
    user: UserRead = Depends(RoleRequired(Role.MANAGER)),
    session: AsyncSession = Depends(get_async_session),
):
    query = select(Ticket).where(Ticket.id == ticket_id)

    ticket = await execute_query_one(session, query)

    ticket.status = TicketStatus.CLOSED

    result = await add_and_commit(session, ticket)

    return result


@router.get("/all_closed", response_model=list[TicketOut])
async def ticket_get_all_my_closed(
    user: UserRead = Depends(RoleRequired(Role.MANAGER)),
    session: AsyncSession = Depends(get_async_session),
):
    query = select(Ticket).where(
        and_(
            Ticket.manager_id == user.id,
            Ticket.status == str(TicketStatus.CLOSED),
        )
    )

    tickets = await execute_query_all(session, query)

    return tickets


@router.post("/message", response_model=MessageOut)
async def message_craete(
    ticket_id: int,
    text: str,
    user: UserRead = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
):
    result = Message(
        text=text,
        ticket_id=ticket_id,
        user_id=user.id,
    )

    result = await add_and_commit(session, result)

    return result
