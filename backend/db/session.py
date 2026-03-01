from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from core.config import settings


postgres_settings = settings.postgres

engine = create_async_engine(
    postgres_settings.DATABASE_URL,
    echo=True,
    future=True
)

AsyncSessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False    
)

async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session