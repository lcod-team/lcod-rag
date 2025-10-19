from functools import lru_cache
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file="config/.env", env_file_encoding="utf-8", extra="ignore")

    # Infrastructure
    ollama_base_url: str = "http://localhost:11434"
    qdrant_url: str = "http://localhost:6333"
    qdrant_api_key: str | None = None
    qdrant_collection: str = "lcod_docs"

    # Models
    embedding_model: str = "nomic-embed-text"
    generative_model: str = "llama3.1"
    top_k: int = 5

    # API
    api_host: str = "0.0.0.0"
    api_port: int = 8088


class CollectionMetadata(BaseModel):
    repo: str | None = None
    path: str | None = None
    heading: str | None = None
    chunk_index: int | None = None


@lru_cache()
def get_settings() -> Settings:
    return Settings()
