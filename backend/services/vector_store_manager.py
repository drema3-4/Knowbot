from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
import os
from langchain_core.documents import Document

from core.config import settings


class VectorStoreManager:
    """Инициализирует векторную БД и ретривера."""
    def __init__(self):
        """Запускает функции по инициализации векторной БД и ретривера."""
        self.__init_vectore_store__()
        self.__init_retriever__()

    def __init_vectore_store__(
        self
    ) -> None:
        """Инициализирует векторную БД."""
        self.vectore_store_settings = settings.vector_store

        self.persist_directory = self.vectore_store_settings.PERSIST_DIRECTORY
        self.embeddings = HuggingFaceEmbeddings(
            **self.vectore_store_settings.get_embeddig_model_settings()
        )

        if os.path.exists(self.persist_directory) and os.listdir(self.persist_directory):
            self.vector_store = Chroma(
                persist_directory=self.persist_directory,
                embedding_function=self.embeddings
            )
        else:
            dummy_doc = Document(
                page_content="placeholder",
                metadata={ "source": "init" }
            )
            self.vector_store = Chroma.from_documents(
                documents=[dummy_doc],
                embedding=self.embeddings,
                persist_directory=self.persist_directory
            )
            self.vector_store._collection.delete(where={ "source": "init" })
    
    def __init_retriever__(
        self
    ) -> None:
        """Инициализирует ретривер."""
        self.retriever = self.vector_store.as_retriever(**self.vectore_store_settings.get_retriever_settings())
    
    def get_vector_store(self):
        """Даёт ссылку на векторное хранилище."""
        return self.vector_store
    
    def get_retriever(self):
        """Даёт ссылку на ретривер."""
        return self.retriever