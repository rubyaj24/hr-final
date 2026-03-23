try:
    # When run as: python -m RAG.test_retriever
    from .retrieval import get_retriever
except ImportError:
    # When run as: python test_retriever.py (inside RAG/)
    from retrieval import get_retriever


if __name__ == "__main__":
    retriever = get_retriever()

    query = "how many employees?"
    docs = retriever.invoke(query)

    for i, doc in enumerate(docs, start=1):
        print(f"\nResult {i}")
        print(doc.page_content)