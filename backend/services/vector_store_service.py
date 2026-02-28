from typing import List
from langchain_core.documents import Document
import os
from pathlib import Path
import pymupdf
import tempfile
import zipfile

from services.document_processor import DocumentProcessor
from core.config import settings

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

    def validate_pdf_by_path(
        self,
        path_document: str
    ) -> bool:
        """Проверяет pdf документ: что с таким именем документа нет, что он не пуст и нужного расширения."""
        path = Path(path_document)

        if not path.suffix.lower() == ".pdf":
            print(f"Файл имеет расширение {path.suffix}, ожидалось .pdf")
            return False
        
        target_path = Path(settings.DOCUMENTS_DIRECTORY) / path.name
        if target_path.exists():
            print(f"Файл '{path.name}' с таким именем уже есть")
            return False

        try:
            if os.path.getsize(path_document) == 0:
                print(f"Файл '{path.name}' пустой")
                return False
            
            with pymupdf.open(path_document) as doc:
                if len(doc) == 0:
                    print(f"Файл '{path.name}' пустой")
                    return False
   
        except:
            print(f"С файлом '{path.name}' что-то не так")
            return False

        return True
    
    def validate_zip_by_path(
        self,
        path_archive: str
    ) -> tuple[bool, List[str], str]:
        temp_dir = settings.UPLOAD_TEMP_DIR
        extract_dir = tempfile.mkdtemp(dir=temp_dir)

        path = Path(path_archive)

        if not path.suffix.lower() == ".zip":
            print(f"Файл имеет расширение {path.suffix}, ожидалось .zip")
            return (False, [], extract_dir)
        
        try:
            with zipfile.ZipFile(path_archive, "r") as zf:
                zf.extractall(extract_dir)

            valid_pdfs = []

            for root, dirs, files in os.walk(extract_dir):
                for file in files:
                    full_path_file = os.path.join(root, file)

                    if self.validate_pdf_by_path(full_path_file):
                        valid_pdfs.append(full_path_file)

        except:
            print(f"С вашим архивом что-то не так")
            return (False, [], extract_dir)
        
        if len(valid_pdfs) > 0:
            return (True, valid_pdfs, extract_dir)
        else:
            return (False, valid_pdfs, extract_dir)

    def add_pdf_document_by_path(
        self,
        path_document: str
    ) -> None:
        """Добавляет pdf документ в векторную БД."""
        print(f"Началась обработка файла '{path_document}'")
        
        document, document_sha1 = self.document_processor.document_processing(path_document)

        chunks, _ = self.document_processor.chunk_file(document, document_sha1)

        self.__add_chunks__(chunks)

        print(f"Обработка файла '{path_document}' завершилась")

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