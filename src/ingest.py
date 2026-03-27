"""Data ingestion and indexing for HR Helpdesk RAG."""

from datasets import load_dataset
from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from .config import (
    CHROMA_PATH,
    CHUNK_SIZE,
    CHUNK_OVERLAP,
    HF_DATASETS,
    MAX_HF_ROWS,
    get_embedding_model,
    ensure_db_dir,
)


def load_hf_dataset(dataset_name: str, max_rows: int = MAX_HF_ROWS) -> list[Document]:
    """Load a HuggingFace dataset."""
    print(f"Loading HuggingFace dataset: {dataset_name}")
    
    ds = load_dataset(dataset_name)
    documents = []
    
    for row in ds["train"]:
        text = " ".join([str(v) for v in row.values()])
        documents.append(Document(page_content=text, metadata={"source": dataset_name}))
        if len(documents) >= max_rows:
            break
    
    print(f"{dataset_name} -> {len(documents)} records")
    return documents


def load_all_datasets() -> list[Document]:
    """Load all HR datasets from HuggingFace."""
    print("Loading all HR datasets...")
    
    documents = []
    
    # HuggingFace datasets
    for dataset in HF_DATASETS:
        try:
            docs = load_hf_dataset(dataset)
            documents.extend(docs)
        except Exception as e:
            print(f"Skipping {dataset}: {e}")
    
    print(f"Total documents loaded: {len(documents)}")
    return documents


def split_documents(documents: list[Document]) -> list[Document]:
    """Split documents into chunks."""
    print("Splitting documents...")
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n\n", "\n", ".", " ", ""]
    )
    
    chunks = text_splitter.split_documents(documents)
    print(f"Total chunks created: {len(chunks)}")
    
    return chunks


def create_vector_store(chunks: list[Document], persist_directory: str = None) -> Chroma:
    """Create and persist the vector store."""
    if persist_directory is None:
        persist_directory = CHROMA_PATH
    
    if not chunks:
        raise ValueError("No chunks provided for indexing")
    
    print(f"Creating vector store at: {persist_directory}")
    ensure_db_dir()
    
    embedding_model = get_embedding_model()
    
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embedding_model,
        persist_directory=persist_directory
    )
    
    print("Vector store created successfully")
    return vectorstore


def ingest() -> None:
    """Main ingestion pipeline."""
    documents = load_all_datasets()
    chunks = split_documents(documents)
    create_vector_store(chunks)
    print("Ingestion complete!")


if __name__ == "__main__":
    load_dotenv()
    ingest()
