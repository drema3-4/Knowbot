from fastapi import FastAPI
from contextlib import asynccontextmanager

from database import create_tables, drop_tables
from router import router as user_router

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