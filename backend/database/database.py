from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import ForeignKey


engine = create_async_engine(
    "sqlite+aiosqlite:///db.db"
)
new_session = async_sessionmaker(engine, expire_on_commit=False)

class Model(DeclarativeBase):
    pass


class UserOrm(Model):
    __tablename__ = "User"

    user_id: Mapped[int] = mapped_column(primary_key=True)


class SessionOrm(Model):
    __tablename__ = "Session"

    session_id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("User.user_id"))


class QueryOrm(Model):
    __tablename__ = "Query"

    query_id: Mapped[int] = mapped_column(primary_key=True)
    session_id: Mapped[int] = mapped_column(ForeignKey("Session.session_id"))
    num_query_in_session: Mapped[int]
    query: Mapped[str]


class AnswerOrm(Model):
    __tablename__ = "Answer"

    answer_id: Mapped[int] = mapped_column(primary_key=True)
    session_id: Mapped[int] = mapped_column(ForeignKey("Session.session_id"))
    num_answer_in_session: Mapped[int]
    answer: Mapped[str]


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.create_all)

async def drop_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.drop_all)