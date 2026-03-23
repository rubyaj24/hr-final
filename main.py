from RAG.bothdataset import load_all_datasets
from RAG.chunking import split_documents
from RAG.embedding import create_vector_store

def main():
    documents = load_all_datasets()
    chunks = split_documents(documents)
    create_vector_store(chunks)

if __name__ == "__main__":
    main()