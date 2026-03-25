"""HR Helpdesk RAG - Core Package."""

from .config import (
    CHROMA_PATH,
    EMBEDDING_MODEL,
    CHUNK_SIZE,
    CHUNK_OVERLAP,
    TOP_K,
    RETRIEVAL_K,
    LLM_MODEL,
    LLM_TEMPERATURE,
    get_embedding_model,
    ensure_db_dir,
)

__all__ = [
    "CHROMA_PATH",
    "EMBEDDING_MODEL",
    "CHUNK_SIZE",
    "CHUNK_OVERLAP",
    "TOP_K",
    "RETRIEVAL_K",
    "LLM_MODEL",
    "LLM_TEMPERATURE",
    "get_embedding_model",
    "ensure_db_dir",
]
