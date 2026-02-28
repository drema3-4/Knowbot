from typing import List
from langchain_core.documents import Document
import os

from services.document_processor import DocumentProcessor

class VectorStoreService:
    """Интерфейс для работы с векторной БД."""
    def __init__(
        self,
        vector_store,
        retriever,
        document_processor: DocumentProcessor
    ):
        """Загружает векторное хранилище, ретривер и обработчик документов в единый объект."""
        self.vector_store = vector_store
        self.retriever = retriever
        self.document_processor = document_processor

    def __add_chunks__(
        self, 
        chunks: List[Document]
    ) -> None:
        """Добавляет чанки документа в векторную БД."""
        self.vector_store.add_documents(chunks)

    def add_pdf_document_by_path(
        self,
        path_document: str
    ) -> None:
        """Добавляет pdf документ в векторную БД."""
        document, document_sha1 = self.document_processor.load_pdf_document(path_document)

        chunks, _ = self.document_processor.chunk_file(document, document_sha1)

        self.__add_chunks__(chunks)

    def add_pdf_documents_by_path(
        self,
        path_documents: str
    ) -> None:
        """Добавляет несколько документов pdf в векторную БД."""
        documents_names = os.listdir(path_documents)

        for doc_name in documents_names:
            try:
                path_pdf_document = os.path.join(path_documents, doc_name)

                self.add_pdf_document_by_path(path_pdf_document)

            except Exception as e:
                continue