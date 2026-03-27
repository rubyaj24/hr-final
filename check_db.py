"""Check ChromaDB vector count."""

import os
from pathlib import Path
from dotenv import load_dotenv
from langchain_chroma import Chroma
from src.config import CHROMA_PATH, get_embedding_model

load_dotenv()

db_path = Path(CHROMA_PATH)

if not db_path.exists():
    print(f"[X] Database not found at: {CHROMA_PATH}")
    print("\nTo create the database, run:")
    print("  python main.py")
else:
    print(f"[OK] Database found at: {CHROMA_PATH}")
    
    try:
        embedding_model = get_embedding_model()
        db = Chroma(
            persist_directory=CHROMA_PATH,
            embedding_function=embedding_model,
        )
        
        # Get collection
        collection = db._collection
        count = collection.count()
        
        print(f"\n[DATA] Vector Count: {count:,} vectors stored")
        
        # Get sample metadata
        if count > 0:
            results = collection.peek(limit=5)
            if results and 'metadatas' in results:
                print("\n[SOURCES] Sample Sources:")
                sources = set()
                for metadata in results['metadatas']:
                    if metadata and 'source' in metadata:
                        sources.add(metadata['source'])
                for source in sources:
                    print(f"  - {source}")
        
    except Exception as e:
        print(f"\n[ERROR] Error reading database: {e}")
