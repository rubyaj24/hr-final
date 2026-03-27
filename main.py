"""HR Helpdesk RAG - Main Entry Point.

Usage:
    python main.py              # Build index
    python main.py --serve     # Build index and start API
"""

import argparse
import sys


def ingest():
    """Run the data ingestion pipeline."""
    from src.ingest import ingest as run_ingest
    print("Starting data ingestion...")
    run_ingest()


def serve():
    """Start the FastAPI server."""
    import uvicorn
    from api.main import app
    
    print("Starting API server on http://0.0.0.0:8000")
    print("Docs available at http://localhost:8000/docs")
    uvicorn.run(app, host="0.0.0.0", port=8000)


def main():
    parser = argparse.ArgumentParser(description="HR Helpdesk RAG System")
    parser.add_argument("--serve", action="store_true", help="Start API server after ingestion")
    args = parser.parse_args()
    
    ingest()
    
    if args.serve:
        serve()


if __name__ == "__main__":
    main()
