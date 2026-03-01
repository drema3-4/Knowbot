from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from sqlalchemy import select

from db.models.message import Message


class MessageRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_dialog_messages(
        self,
        user_id: int,
        dialog_id: int
    ) -> List[Message]:
        smtm = select(Message).where(
            Message.user_id == user_id,
            Message.dialog_id == dialog_id
        ).order_by(Message.created_at)
        result = await self.session.execute(smtm)
        return result.scalars().all()
    
    async def add_message(
        self,
        user_id: int,
        dialog_id: int,
        content: str,
        role: str
    ) -> Message:
        new_message = Message(
            user_id=user_id,
            dialog_id=dialog_id,
            content=content,
            role=role
        )
        self.session.add(new_message)
        await self.session.commit()
        await self.session.refresh(new_message)
        return new_message