from document_processor import DocumentProcessor
from typing import List
from langchain_core.documents import Document
import os

class VectorStoreService:
    def __init__(
        self,
        vector_store,
        retriever,
        document_processor: DocumentProcessor
    ):
        self.vector_store = vector_store
        self.retriever = retriever
        self.document_processor = document_processor

    def __add_chunks__(
        self, 
        chunks: List[Document]
    ) -> None:
        self.vector_store.add_documents(chunks)

    def add_pdf_document_by_path(
        self,
        path_document: str
    ) -> None:
        document, document_sha1 = self.document_processor.load_pdf_document(path_document)

        chunks, _ = self.document_processor.chunk_file(document, document_sha1)

        self.__add_chunks__(chunks)

    def add_pdf_documents_by_path(
        self,
        path_documents: str
    ) -> None:
        documents_names = os.listdir(path_documents)

        for doc_name in documents_names:
            try:
                path_pdf_document = os.path.join(path_documents, doc_name)

                self.add_pdf_document_by_path(path_pdf_document)

            except Exception as e:
                continue