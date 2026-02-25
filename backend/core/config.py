from typing import Dict, Any
from pathlib import Path
from pydantic_settings import BaseSettings

class Vector_Store_Settings(BaseSettings):
    EMBEDDING_MODEL_SETTINGS: Dict[str, Any] = {
        "model_name": "all-MiniLM-L6-v2",
        "model_kwargs": { "device": "cpu" },
        "encode_kwargs": { "normalize_embeddings": True }
    }

    RETRIEVER_SETTINGS: dict[str, Any] = {
        "search_type": "mmr",
        "search_kwargs": {
            "k": 5,
            "fetch_k": 20,
            "lambda_mult": 0.5
        }
    }

    PERSIST_DIRECTORY: Path = Path(__file__).parent.parent / "chroma_db"

class Text_Splitter_Settings(BaseSettings):
    CHUNK_SIZE: int = 1000
    CHUNK_OVERLAP: int = 200
    MIN_CHUNK_SIZE: int = 50
    LENGTH_FUNCTION = len
    SEPARATORS = [     # Иерархия разделителей (от крупных к мелким)
        "\n\n",        # Двойные переносы строк - границы между абзацами
        "\n",          # Одиночные переносы строк
        ". ",          # Конец предложений с пробелом
        "? ", "! ",    # Вопросительные и восклицательные знаки
        "; ", ": ",    # Точки с запятой и двоеточия
        ", ",          # Запятые
        " ",           # Пробелы между словами
        ""             # Последний резервный вариант
    ]

    def to_langchain_params(self) -> dict:
        return {
            "chunk_size": self.CHUNK_SIZE,
            "chunk_overlap": self.CHUNK_OVERLAP,
            "length_function": self.LENGTH_FUNCTION,
            "separators": self.SEPARATORS
        }

class LLM_Settings(BaseSettings):
    API_KEY: str
    MODEL="gemini-2.5-flash"
    TEMPERATURE=0.1
    MAX_TOKENS=None
    TIMEOUT=None
    MAX_RETRIES=2

    def to_langchain_params(self) -> dict:
        return {
            "api_key": self.API_KEY,
            "model": self.MODEL,
            "temperature": self.TEMPERATURE,
            "max_tokens": self.MAX_TOKENS,
            "timeout": self.TIMEOUT,
            "max_retries": self.MAX_RETRIES
        }
    
    class Config:
        env_file = Path(__file__).parent.parent / ".env"

class Settings(BaseSettings):
    vector_store: Vector_Store_Settings = Vector_Store_Settings()
    text_splitter: Text_Splitter_Settings = Text_Splitter_Settings()
    llm: LLM_Settings = LLM_Settings()

    class Config:
        env_file = Path(__file__).parent.parent / ".env"

settings = Settings()