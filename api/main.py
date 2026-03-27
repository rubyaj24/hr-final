"""FastAPI server for HR Helpdesk RAG."""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from src.query import query_rag


app = FastAPI(title="HR Helpdesk API", version="1.0.0")


class AskRequest(BaseModel):
    query: str


class SourceItem(BaseModel):
    source: str


class AskResponse(BaseModel):
    query: str
    answer: str
    sources: list[SourceItem]


@app.post("/ask", response_model=AskResponse)
def ask(request: AskRequest):
    """Process an HR question and return an answer."""
    try:
        result = query_rag(request.query)
        return AskResponse(
            query=request.query,
            answer=result["answer"],
            sources=result["sources"],
        )
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@app.get("/health")
def health():
    """Health check endpoint."""
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
