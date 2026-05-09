import os
from pathlib import Path
from dotenv import load_dotenv
from pydantic import BaseModel, Field


load_dotenv()

def _read_groq_api_key() -> str | None:
    key = os.getenv("GROQ_API_KEY") or os.getenv("CHATGROQ_API_KEY")
    return key.strip() if key and key.strip() else None


class Settings(BaseModel):
    data_dir: Path = Field(default=Path("data/knowledge_base"))
    persist_dir: Path = Field(default=Path("data/chroma"))
    collection_name: str = Field(default="rag_demo")
    embedding_model: str = Field(default="sentence-transformers/all-MiniLM-L6-v2")
    top_k: int = Field(default=5)
    rerank_top_k: int = Field(default=3)
    groq_api_key: str | None = Field(default_factory=_read_groq_api_key)
    groq_model: str = Field(
        default_factory=lambda: os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")
    )


settings = Settings()