from sqlalchemy.ext.asyncio import AsyncSession

from db.models.dialog import Dialog


class DialogRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_dialog(self, user_id: int) -> Dialog:
        new_dialog = Dialog(
            user_id=user_id
        )
        self.session.add(new_dialog)
        await self.session.commit()
        await self.session.refresh(new_dialog)
        return new_dialog