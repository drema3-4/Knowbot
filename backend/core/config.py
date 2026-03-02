from typing import Dict, Any, Callable, List
from pathlib import Path
from pydantic_settings import BaseSettings


class Vector_Store_Settings(BaseSettings):
    EMBEDDING_MODEL_NAME: str = "all-MiniLM-L6-v2"
    EMBEDDING_MODEL_KWARGS: Dict[str, Any] = { "device": "cpu" }
    EMBEDDING_ENCODE_KWARGS: Dict[str, Any] = { "normalize_embeddings": True }

    RETRIEVER_SEARCH_TYPE: str = "mmr"
    RETRIEVER_SEARCH_KWARGS: Dict[str, Any] = {
        "k": 5,
        "fetch_k": 20,
        "lambda_mult": 0.5
    }

    PERSIST_DIRECTORY: Path = Path(__file__).parent.parent / "chroma_db"


    def get_embeddig_model_settings(self) -> Dict[str, Any]:
        return {
            "model_name": self.EMBEDDING_MODEL_NAME,
            "model_kwargs": self.EMBEDDING_MODEL_KWARGS,
            "encode_kwargs": self.EMBEDDING_ENCODE_KWARGS
        }

    def get_retriever_settings(self) -> Dict[str, Any]:
        return {
            "search_type": self.RETRIEVER_SEARCH_TYPE,
            "search_kwargs": self.RETRIEVER_SEARCH_KWARGS
        }


class Text_Splitter_Settings(BaseSettings):
    CHUNK_SIZE: int = 1000
    CHUNK_OVERLAP: int = 200
    MIN_CHUNK_SIZE: int = 50
    LENGTH_FUNCTION: Callable = len
    SEPARATORS: List[str] = [     # Иерархия разделителей (от крупных к мелким)
        "\n\n",        # Двойные переносы строк - границы между абзацами
        "\n",          # Одиночные переносы строк
        ". ",          # Конец предложений с пробелом
        "? ", "! ",    # Вопросительные и восклицательные знаки
        "; ", ": ",    # Точки с запятой и двоеточия
        ", ",          # Запятые
        " ",           # Пробелы между словами
        ""             # Последний резервный вариант
    ]

    def get_text_splitter_settings(self) -> Dict[str, Any]:
        return {
            "chunk_size": self.CHUNK_SIZE,
            "chunk_overlap": self.CHUNK_OVERLAP,
            "length_function": self.LENGTH_FUNCTION,
            "separators": self.SEPARATORS
        }


class LLM_Settings(BaseSettings):
    API_KEY: str
    MODEL: str = "openai/gpt-4o-mini"
    BASE_URL: str = "https://api.vsegpt.ru/v1"
    TEMPERATURE: float = 0.1
    MAX_TOKENS: Any = None
    TIMEOUT: Any = None
    MAX_RETRIES: int = 2

    def get_llm_settings(self) -> Dict[str, Any]:
        return {
            "api_key": self.API_KEY,
            "model": self.MODEL,
            "base_url": self.BASE_URL,
            "temperature": self.TEMPERATURE,
            "max_tokens": self.MAX_TOKENS,
            "timeout": self.TIMEOUT,
            "max_retries": self.MAX_RETRIES
        }
    
    class Config:
        env_file = Path(__file__).parent.parent / ".env"
        extra = "ignore"


class PostgresSettings(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str = "db"
    POSTGRES_PORT: str = "5432"

    @property
    def DATABASE_URL(self) -> str:
        """Собираем URL для подключения к БД (асинхронный драйвер asyncpg)."""
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    class Config:
        env_file = Path(__file__).parent.parent / ".env"
        extra = "ignore"

class Settings(BaseSettings):
    vector_store: Vector_Store_Settings = Vector_Store_Settings()
    text_splitter: Text_Splitter_Settings = Text_Splitter_Settings()
    llm: LLM_Settings = LLM_Settings()
    postgres: PostgresSettings = PostgresSettings()

    DOCUMENTS_DIRECTORY: Path = Path(__file__).parent.parent / "documents"

    UPLOAD_TEMP_DIR: Path = Path(__file__).parent.parent / "upload_tmp_dir"

    class Config:
        env_file = Path(__file__).parent / ".env"


settings = Settings()