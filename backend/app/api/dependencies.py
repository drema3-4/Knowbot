from fastapi import Request
from services.rag_engine import RAGEngine
from services.vector_store_service import VectorStoreService

def get_rag_engine(request: Request) -> RAGEngine:
    return request.app.state.rag_engine

def get_vector_store_service(request: Request) -> VectorStoreService:
    return request.app.state.vector_store_service