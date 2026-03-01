from sqlalchemy import Column, Integer, ForeignKey, String, DateTime, Index
from sqlalchemy.sql import func

from db.base import Base


class Message(Base):
    __tablename__ = "messages"

    message_id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False, index=True)
    dialog_id = Column(Integer, ForeignKey("dialogs.dialog_id"), nullable=False, index=True)

    content = Column(String, nullable=False)
    role = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        Index("ix_messages_dialog_id_created_at", message_id, dialog_id, created_at.asc())
    )