import os
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from chunking import main as chunking_main


def create_vector_store(chunks, persist_directory="db/chroma_db"):
    """
    Create and store embeddings in ChromaDB.

    Parameters
    ----------
    chunks : Sequence[Document] or list[str]
        The documents/texts to embed and index. Must be non-empty.
    persist_directory : str
        Directory path where the Chroma database will be written.
    """

    if not chunks:
        raise ValueError("`chunks` argument is empty; nothing to index.")

    print("Creating embeddings and storing in ChromaDB...")

    # Open-source embedding model.  We switched to the new package to avoid
    # LangChain deprecation warnings and the need for sentence-transformers
    embedding_model = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    print("--- Creating vector store ---")

    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embedding_model,
        persist_directory=persist_directory
    )

    print("--- Vector store creation complete ---")
    print(f"Vector database saved at: {persist_directory}")

    return vectorstore

def main():
    # Call the chunking main function and get the chunks
    chunks = chunking_main()
    # Create the vector store with the chunks
    vectorstore = create_vector_store(chunks)
    print("Vector store creation process completed.")

# ---------------------------------------------------------------------------
# example script entrypoint when run directly; keeps module import-safe
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    main()
