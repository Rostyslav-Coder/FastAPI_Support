"""src/ticket/routers.py"""

from fastapi import APIRouter, Depends, HTTPException
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
async def create_ticket(
    ticket: TicketIn,
    user: UserRead = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
):
    if user.role != str(Role.USER):
        raise HTTPException(status_code=403, detail="No permission")

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
