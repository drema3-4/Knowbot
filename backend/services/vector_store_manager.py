from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
import os
from langchain_core.documents import Document

from core.config import settings


class VectorStoreManager:
    def __init__(self):
        self.__init_vectore_store__()
        self.__init_retriever__()

    def __init_vectore_store__(
        self
    ) -> None:
        self.vectore_store_settings = settings.vector_store

        self.presist_directory = self.vectore_store_settings.PERSIST_DIRECTORY
        self.embeddings = HuggingFaceEmbeddings(
            **self.vectore_store_settings.EMBEDDING_MODEL_SETTINGS
        )

        if os.path.exists(self.presist_directory) and os.listdir(self.presist_directory):
            # Загружаем существующую базу данных
            self.vector_store = Chroma(
                persist_directory=self.presist_directory,
                embedding_function=self.embeddings
            )
        else:
            # Создаем новую базу с фиктивным документом
            dummy_doc = Document(
                page_content="placeholder",
                metadata={ "source": "init" }
            )
            self.vector_store = Chroma.from_documents(
                documents=[dummy_doc],
                embedding=self.embeddings,
                persist_directory=self.presist_directory
            )
            # Удаляем фиктивный документ
            self.vector_store._collection.delete(where={ "source": "init" })
    
    def __init_retriever__(
        self
    ) -> None:
        self.retriever = self.vector_store.as_retriever(**self.vectore_store_settings.RETRIEVER_SETTINGS)
    
    def get_vector_store(self):
        return self.vector_store
    
    def get_retriever(self):
        return self.retriever