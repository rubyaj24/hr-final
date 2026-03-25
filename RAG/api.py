from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from generation import generate_answer

app = FastAPI(title="HR Helpdesk API")


class AskRequest(BaseModel):
    query: str


@app.post("/ask")
def ask(request: AskRequest):
    try:
        answer = generate_answer(request.query)

        return {
            "query": request.query,
            "answer": answer
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
def health():
    return {"status": "ok"}