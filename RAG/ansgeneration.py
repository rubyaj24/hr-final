import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings


def dedupe_docs(docs, max_docs=5):
    seen = set()
    unique = []
    for doc in docs:
        content = " ".join(doc.page_content.split())
        if not content:
            continue
        key = content.lower()
        if key in seen:
            continue
        seen.add(key)
        unique.append(doc)
        if len(unique) >= max_docs:
            break
    return unique


def main():
    # Load .env from the same folder as this script
    env_path = Path(__file__).resolve().parent / ".env"
    load_dotenv(env_path)

    groq_key = os.getenv("groq_key")
    if not groq_key:
        raise RuntimeError(
            "Missing GROQ_API_KEY. Set environment variable or add it to RAG/.env"
        )

    persistent_directory = str(Path(__file__).resolve().parent / "db" / "chroma_db")

    embedding_model = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    db = Chroma(
        persist_directory=persistent_directory,
        embedding_function=embedding_model,
    )

    query = "What is the leave policy?"
    retriever = db.as_retriever(search_kwargs={"k": 8})
    retrieved_docs = retriever.invoke(query)
    relevant_docs = dedupe_docs(retrieved_docs, max_docs=5)

    print(f"\nUser Query: {query}")
    print("\n--- Retrieved Context (Deduplicated) ---\n")
    for i, doc in enumerate(relevant_docs, 1):
        print(f"Document {i}:")
        print(doc.page_content)
        print()

    combined_input = f"""
Based on the following HR documents, answer the question.

Question:
{query}

Documents:
{chr(10).join([f"- {doc.page_content}" for doc in relevant_docs])}

Provide a clear HR policy answer using only the provided documents.
If the information is not available, say:
"I don't have enough information from the documents."
"""

    model = ChatGroq(
        model="llama3-8b-instant",
        temperature=0,
        api_key=groq_key,
    )

    messages = [
        SystemMessage(content="You are an HR helpdesk assistant."),
        HumanMessage(content=combined_input),
    ]

    result = model.invoke(messages)

    print("\n--- Generated Response ---\n")
    print(result.content)


if __name__ == "__main__":
    main()