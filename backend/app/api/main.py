from contextlib import asynccontextmanager
from fastapi import FastAPI
import shutil
from pathlib import Path

from core.config import settings
from services.document_processor import DocumentProcessor
from services.vector_store_manager import VectorStoreManager
from services.rag_engine import RAGEngine
from services.vector_store_service import VectorStoreService
from api.routers import query

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 1. Полностью удаляем старую базу данных (чтобы гарантировать свежесть)
    persist_dir = settings.vector_store.PERSIST_DIRECTORY
    if persist_dir.exists():
        shutil.rmtree(persist_dir)
        print(f"Старая база удалена: {persist_dir}")

    # 2. Инициализируем сервисы (менеджер создаст новую пустую базу)
    document_processor = DocumentProcessor()
    vector_store_manager = VectorStoreManager()   # внутри создаст пустую Chroma
    rag_engine = RAGEngine(retriever=vector_store_manager.get_retriever())
    vector_store_service = VectorStoreService(
        vector_store=vector_store_manager.get_vector_store(),
        retriever=vector_store_manager.get_retriever(),
        document_processor=document_processor
    )

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