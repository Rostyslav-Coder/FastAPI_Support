"""src/ticket/utils.py"""

from sqlalchemy.ext.asyncio import AsyncSession

from src.ticket.schemas import TicketOut


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
