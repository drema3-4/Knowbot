import re
from typing import List, Tuple
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_core.documents import Document
import hashlib
from langchain_text_splitters import RecursiveCharacterTextSplitter
from ..core.config import settings


class Document_processor:
    def __init__(self):
        self.text_splitter_settings = settings.text_splitter

    def normalize_document(self, document: str) -> str:
        # Замена переносов строк внутри предложений на пробелы
        # Шаблон ищет последовательность: буква/цифра -> перенос строки -> буква/цифра
        document = re.sub(r'(?<=[а-яёa-z0-9])\s*\n\s*(?=[а-яёa-z0-9])', ' ', document, flags=re.IGNORECASE)
        
        # Замена нескольких пробельных символов на один пробел
        document = re.sub(r'\s+', ' ', document)
        
        # Удаление пробелов перед знаками препинания
        document = re.sub(r'\s+([.,!?;:])', r'\1', document)
        
        # Восстановление переносов строк после завершающих предложение знаков
        # Восстанавливает структуру абзацев
        document = re.sub(r'([.!?])\s+([А-ЯA-Z])', r'\1\n\n\2', document)
        
        return document.strip()
    
    # затычка (временное решение)
    def load_pdf_document(self, path_document: str) -> Tuple[List[Document], str]:
        # Инициализация загрузчика PyMuPDF с отключением извлечения изображений
        loader = PyMuPDFLoader(
            path_document,
            extract_images=False  # Извлечение только текста для уменьшения объема данных
        )
        
        # Загрузка документа: возвращает список Document объектов (по одному на страницу)
        document = loader.load()
        
        # Обработка каждой страницы документа
        for doc in document:
            # Нормализация текста страницы
            doc.page_content = self.normalize_document(doc.page_content)
            
            # Сохранение номера страницы в метаданных
            # PyMuPDFLoader сохраняет номер страницы в metadata['page']
            if 'page' in doc.metadata:
                # Преобразование номера страницы в целое число
                # page_index представляет физический номер страницы (начиная с 0)
                doc.metadata['page_index'] = int(doc.metadata['page'])
            else:
                # Резервное значение, если номер страницы не найден
                doc.metadata['page_index'] = 0
        
        # Вычисление SHA1 хэша исходного PDF файла для идентификации
        with open(path_document, "rb") as f:
            document_bytes = f.read()
            document_sha1 = hashlib.sha1(document_bytes).hexdigest()
        
        # Добавление идентификационной информации в метаданные каждой страницы
        for doc in document:
            doc.metadata['pdf_sha1'] = document_sha1  # Уникальный идентификатор документа
            doc.metadata['source_path'] = path_document  # Путь к исходному файлу
        
        return document, document_sha1

    def chunk_file(self, document: List[Document], document_sha1: str) -> Tuple[List[Document], str]:
        # Инициализация рекурсивного текстового сплиттера
        text_splitter = RecursiveCharacterTextSplitter(
            **self.text_splitter_settings.to_langchain_params()
        )
        
        # Разбиение документа на чанки
        chunks = text_splitter.split_documents(document)
        
        # Фильтрация слишком маленьких чанков
        # Удаляются чанки размером менее MIN_CHUNK_SIZE символов (без учета пробелов)
        chunks = [
            chunk for chunk in chunks 
            if len(chunk.page_content.strip()) >= self.text_splitter_settings.MIN_CHUNK_SIZE
        ]
        
        # Добавление SHA1 хэша в метаданные каждого чанка
        # Это позволяет отслеживать происхождение чанка даже после разбиения
        for chunk in chunks:
            chunk.metadata["pdf_sha1"] = document_sha1
        
        return chunks, document_sha1