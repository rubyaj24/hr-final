from pathlib import Path
from functools import lru_cache
from typing import Any

from fastapi import FastAPI, HTTPException
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from pydantic import BaseModel, Field

# Import your modules
try:
    from .bothdataset import load_all_datasets
    from .chunking import split_documents
    from .embedding import create_vector_store
except ImportError:
    from bothdataset import load_all_datasets
    from chunking import split_documents
    from embedding import create_vector_store


# ================= CONFIG =================
PERSIST_DIRECTORY = str(Path(__file__).resolve().parent / "db" / "chroma_db")
TOP_K = 3
REBUILD_INDEX_ON_START = False  # IMPORTANT: avoid rebuilding every time


# ================= VECTOR STORE =================
def build_or_load_vectorstore():
    embedding_model = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    # Load DB
    vectorstore = Chroma(
        persist_directory=PERSIST_DIRECTORY,
        embedding_function=embedding_model,
    )

    return vectorstore


# ================= RETRIEVER =================
@lru_cache(maxsize=1)
def get_retriever():
    vectorstore = build_or_load_vectorstore()

    retriever = vectorstore.as_retriever(
        search_kwargs={"k": TOP_K}
    )

    print("Retriever initialized")
    return retriever


# ================= FASTAPI =================
app = FastAPI(title="HR Retrieval API")


# ================= REQUEST/RESPONSE =================
class RetrieveRequest(BaseModel):
    query: str = Field(..., min_length=1)


class RetrievedDocument(BaseModel):
    content: str
    metadata: dict[str, Any]


# ================= ENDPOINT =================
@app.post("/retrieve", response_model=RetrievedDocument)
def retrieve(request: RetrieveRequest):
    try:
        retriever = get_retriever()

        docs = retriever.invoke(request.query)

        # ❌ No result
        if not docs:
            raise HTTPException(status_code=404, detail="No documents found")

        # ✅ Return ONLY first result
        first_doc = docs[0]
        content = first_doc.page_content

        # Extract only bot response
        if "<bot>:" in content:
            answer = content.split("<bot>:")[-1].strip()
        else:
            answer = content.strip()

        return RetrievedDocument(
            content=first_doc.page_content,
            metadata=first_doc.metadata
        )

    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


# ================= HEALTH =================
@app.get("/health")
def health():
    return {"status": "ok"}