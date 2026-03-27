"""Shared configuration for the HR Helpdesk RAG system."""

from pathlib import Path
from langchain_huggingface import HuggingFaceEmbeddings

# Project paths
BASE_DIR = Path(__file__).resolve().parent.parent
DB_DIR = BASE_DIR / "src" / "db"
CHROMA_PATH = str(DB_DIR / "chroma_db")

# Embedding settings
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# Chunking settings
CHUNK_SIZE = 800
CHUNK_OVERLAP = 100

# Retrieval settings
TOP_K = 3
RETRIEVAL_K = 8

# LLM settings
LLM_MODEL = "llama-3.1-8b-instant"
LLM_TEMPERATURE = 0

# Data sources (only HR Policy Q&A datasets)
HF_DATASETS = [
    "EmbraceCoder/HR_Policy",
    "Synkro123/hr-policy-traces"
]

# Kaggle datasets removed - they contain raw employee data, not HR policies

MAX_HF_ROWS = 2000


def get_embedding_model():
    """Get the embedding model instance."""
    return HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)


def ensure_db_dir():
    """Ensure the database directory exists."""
    DB_DIR.mkdir(parents=True, exist_ok=True)
