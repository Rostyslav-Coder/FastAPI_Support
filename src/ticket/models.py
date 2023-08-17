"""src/ticket/models.py"""

from datetime import datetime

from sqlalchemy import TIMESTAMP, Boolean, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base
from src.ticket.constants import TicketStatus


class Ticket(Base):
    """Class used to create Ticket in DB"""

    __tablename__ = "tickets"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    title: Mapped[str] = mapped_column(String(length=100), nullable=False)
    text: Mapped[str] = mapped_column(String(length=4000), nullable=False)
    visibility: Mapped[bool] = mapped_column(Boolean, default=True)
    status: Mapped[int] = mapped_column(
        Integer, default=TicketStatus.NOT_STARTED
    )
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    manager_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id"), nullable=True
    )
    user = relationship(
        "User", back_populates="tickets", foreign_keys=[user_id]
    )
    manager = relationship("User", foreign_keys=[manager_id])
    messages = relationship("Message", back_populates="ticket")


class Message(Base):
    """Class used to create Message in DB"""

    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    text: Mapped[str] = mapped_column(String(length=4000), nullable=False)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    ticket_id: Mapped[int] = mapped_column(Integer, ForeignKey("tickets.id"))
    timestamp: Mapped[TIMESTAMP] = mapped_column(
        TIMESTAMP, default=datetime.utcnow
    )
    user = relationship("User", back_populates="messages")
    ticket = relationship("Ticket", back_populates="messages")
