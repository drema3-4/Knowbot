from contextlib import asynccontextmanager
# from fastapi import FastAPI
from fastapi_offline import FastAPIOffline as FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

from core.config import settings
from services.document_processor import DocumentProcessor
from services.vector_store_manager import VectorStoreManager
from services.rag_engine import RAGEngine
from services.vector_store_service import VectorStoreService
from api.routers import query, upload, users, dialogs
from api.routers import upload
from db.session import engine
from db.base import Base


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    document_directory = settings.DOCUMENTS_DIRECTORY
    os.makedirs(document_directory, exist_ok=True)

    upload_temp_directory = settings.UPLOAD_TEMP_DIR
    os.makedirs(upload_temp_directory, exist_ok=True)

    # 1. Инициализируем сервисы (менеджер создаст новую пустую базу)
    document_processor = DocumentProcessor()
    vector_store_manager = VectorStoreManager()   # внутри создаст пустую Chroma
    rag_engine = RAGEngine(retriever=vector_store_manager.get_retriever())
    vector_store_service = VectorStoreService(
        vector_store=vector_store_manager.get_vector_store(),
        retriever=vector_store_manager.get_retriever(),
        document_processor=document_processor
    )

    app.state.vector_store_service = vector_store_service

    # 3. Автоматически загружаем все PDF из заданной папки
    docs_dir = settings.DOCUMENTS_DIRECTORY
    if docs_dir.exists():
        print(f"Загружаем документы из {docs_dir}")
        vector_store_service.add_pdf_documents_by_path(str(docs_dir))
        print("Загрузка завершена")
    else:
        print(f"Папка {docs_dir} не найдена, документы не загружены")

    # Сохраняем сервисы в app.state
    app.state.rag_engine = rag_engine
    # Другие сервисы сохранять не обязательно, если не нужны в других эндпоинтах

    yield

    # Здесь можно добавить cleanup, если требуется

app = FastAPI(title="RAG MVP", lifespan=lifespan)

app.include_router(query.router, prefix="/api/v1", tags=["Query"])
app.include_router(upload.router, prefix="/api/v1", tags=["Upload"])
app.include_router(users.router, prefix="/api/v1", tags=["Users"])
app.include_router(dialogs.router, prefix="/api/v1", tags=["Dialogs"])

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost",        # для продакшена
        "http://127.0.0.1",        # на всякий случай
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)