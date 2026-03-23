from pathlib import Path
from functools import lru_cache
from typing import Any

from fastapi import FastAPI, HTTPException
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from pydantic import BaseModel, Field

# Support both:
# 1) python -m RAG.retrieval  (preferred)
# 2) python RAG/retrieval.py
try:
    from .bothdataset import load_all_datasets
    from .chunking import split_documents
    from .embedding import create_vector_store
except ImportError:
    from bothdataset import load_all_datasets
    from chunking import split_documents
    from embedding import create_vector_store


PERSIST_DIRECTORY = str(Path(__file__).resolve().parent / "db" / "chroma_db")
TOP_K = 3
REBUILD_INDEX_ON_START = True


def build_or_load_vectorstore(
    persist_directory=PERSIST_DIRECTORY,
    rebuild_index=REBUILD_INDEX_ON_START,
):
    embedding_model = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    if rebuild_index:
        print("Loading datasets...")
        docs = load_all_datasets()

        print("Chunking documents...")
        chunks = split_documents(docs, chunk_size=800, chunk_overlap=100)

        print("Creating vector store...")
        create_vector_store(chunks, persist_directory=persist_directory)

    print("Loading vector database...")
    vectorstore = Chroma(
        persist_directory=persist_directory,
        embedding_function=embedding_model,
    )
    return vectorstore


def get_retriever(
    persist_directory=PERSIST_DIRECTORY,
    k=TOP_K,
    rebuild_index=False,
):
    vectorstore = build_or_load_vectorstore(
        persist_directory=persist_directory,
        rebuild_index=rebuild_index,
    )

    retriever = vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": k},
    )

    print("Retriever initialized")
    return retriever


def retrieve_documents(
    query,
    k=TOP_K,
    persist_directory=PERSIST_DIRECTORY,
    rebuild_index=False,
):
    retriever = get_retriever(
        persist_directory=persist_directory,
        k=k,
        rebuild_index=rebuild_index,
    )
    return retriever.invoke(query)


app = FastAPI(title="HR Retrieval API", version="1.0.0")


class RetrieveRequest(BaseModel):
    query: str = Field(..., min_length=1, description="Query to search against HR docs")
    k: int = Field(TOP_K, ge=1, le=20, description="Number of results")


class RetrievedDocument(BaseModel):
    content: str
    metadata: dict[str, Any]


class RetrieveResponse(BaseModel):
    query: str
    count: int
    results: list[RetrievedDocument]


@lru_cache(maxsize=1)
def get_cached_retriever():
    # Loads once to keep API requests fast.
    return get_retriever(
        persist_directory=PERSIST_DIRECTORY,
        k=TOP_K,
        rebuild_index=REBUILD_INDEX_ON_START,
    )


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/retrieve", response_model=RetrieveResponse)
def retrieve(request: RetrieveRequest):
    try:
        retriever = get_cached_retriever()
        retriever.search_kwargs["k"] = request.k
        docs = retriever.invoke(request.query)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Retrieval failed: {exc}")

    results = [
        RetrievedDocument(content=doc.page_content, metadata=doc.metadata)
        for doc in docs
    ]

    return RetrieveResponse(
        query=request.query,
        count=len(results),
        results=results,
    )


def main():
    query = "What is the leave policy?"

    print(f"\nQuery: {query}")
    results = retrieve_documents(query, rebuild_index=REBUILD_INDEX_ON_START)

    for i, doc in enumerate(results, start=1):
        print(f"\nResult {i}")
        print("Metadata:", doc.metadata)
        print(doc.page_content[:800])


if __name__ == "__main__":
    main()