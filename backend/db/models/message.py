from sqlalchemy import Column, Integer, ForeignKey
from db.base import Base


class Message(Base):
    __tablename__ = "messages"

    user_id = Column(Integer, ForeignKey("users.user_id"), primary_key=True, index=True)
    dialog_id = Column(Integer, ForeignKey("dialogs.dialog_id"), primary_key=True, index=True)
    message_id = Column(Integer, primary_key=True, index=True)