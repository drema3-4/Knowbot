from fastapi import FastAPI
from contextlib import asynccontextmanager
from database.database import create_tables, drop_tables
from api.user_routers import user_router
from api.session_router import session_router
from api.query_router import query_router
from api.answer_router import answer_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    await drop_tables()
    print("Таблицы удалены")
    await create_tables()
    print("Таблицы созданы")
    yield
    print("Выключение")

app = FastAPI(lifespan=lifespan)
app.include_router(user_router)
app.include_router(session_router)
app.include_router(query_router)
app.include_router(answer_router)