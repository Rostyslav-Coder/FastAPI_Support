"""src/ticket/schemas.py"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict

from src.ticket.models import TicketStatus


class TicketIn(BaseModel):
    """Ticket Data Input Model"""

    title: str
    text: str


class TicketOut(TicketIn):
    """Ticket Data Output Model"""

    id: int
    status: TicketStatus
    user_id: int
    manager_id: Optional[int]

    __config__ = ConfigDict(from_attributes=True)


class MessageIn(BaseModel):
    """Message Data Input Model"""

    text: str
    user_id: int
    ticket_id: int


class MessageOut(MessageIn):
    """Message Data Output Model"""

    timestamp: datetime

    __config__ = ConfigDict(from_attributes=True)


class TicketMessageOut(BaseModel):
    ticket: TicketOut
    messages: list[MessageOut]
