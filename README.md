# HR Helpdesk RAG System

A Retrieval-Augmented Generation (RAG) system for HR helpdesk Q&A, built with Python, FastAPI, and Streamlit.

## Features

- **RAG Pipeline**: Combines vector search with LLM generation for accurate HR answers
- **Data Sources**: Loads HR policies from HuggingFace and Kaggle datasets
- **FastAPI Backend**: RESTful API for querying the knowledge base
- **Streamlit UI**: User-friendly chat interface for employees

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
cp .env.example .env
```

Edit `.env` and add your Groq API key:
```
GROQ_API_KEY=your_groq_api_key_here
```

### 3. Build Vector Store (One-time)

```bash
python main.py
```

This loads ~8,000 HR documents and creates the vector index.

### 4. Start the API Server

```bash
uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload
```

API docs available at: http://localhost:8000/docs

### 5. Start the UI

```bash
streamlit run ui/chat.py
```

## Project Structure

```
hr-final/
├── main.py              # Entry point
├── src/                 # Core RAG logic
│   ├── config.py       # Shared configuration
│   ├── ingest.py       # Data loading & indexing
│   └── query.py        # RAG query processing
├── api/                 # FastAPI server
│   └── main.py         # REST API endpoints
├── ui/                  # Streamlit UI
│   └── chat.py         # Chat interface
└── .env                # Environment variables
```

## API Usage

### Query Endpoint

```bash
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"query": "What is the leave policy?"}'
```

Response:
```json
{
  "query": "What is the leave policy?",
  "answer": "Based on the provided HR documents...",
  "sources": [{"source": "EmbraceCoder/HR_Policy"}]
}
```

### Health Check

```bash
curl http://localhost:8000/health
```

## Architecture

```
User Input → API /ask → Query Engine → ChromaDB (vector search)
                                         ↓
                                   Retrieved Docs
                                         ↓
                                   Groq LLM (llama-3.1-8b-instant)
                                         ↓
                                   Generated Answer
```

## Technology Stack

| Component | Technology |
|-----------|------------|
| LLM | Groq (llama-3.1-8b-instant) |
| Embeddings | sentence-transformers/all-MiniLM-L6-v2 |
| Vector DB | ChromaDB |
| API | FastAPI |
| UI | Streamlit |
| Data | HuggingFace + Kaggle datasets |

## Configuration

Settings are centralized in `src/config.py`:

```python
CHUNK_SIZE = 800
CHUNK_OVERLAP = 100
TOP_K = 3              # Documents returned
RETRIEVAL_K = 8        # Documents retrieved before dedup
LLM_MODEL = "llama-3.1-8b-instant"
```

## License

MIT
