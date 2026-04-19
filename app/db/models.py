from app.db.base import Base

from sqlalchemy import String, DateTime, func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from datetime import datetime
from typing import List

class User(Base):
    """ORM-модель пользователя."""
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    role: Mapped[str] = mapped_column(String(50), default="user")
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    messages: Mapped[List["ChatMessage"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )


class ChatMessage(Base):
    """ORM-модель сообщения чата."""
    __tablename__ = "chat_message"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    role: Mapped[str] = mapped_column(String(50))
    content: Mapped[str] = mapped_column(String(5000))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    user: Mapped["User"] = relationship(back_populates="messages")