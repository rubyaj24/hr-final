from langchain_text_splitters import RecursiveCharacterTextSplitter
from bothdataset import load_all_datasets

def split_documents(documents,
                    chunk_size=800,
                    chunk_overlap=100):
    """
    Split documents into smaller chunks
    """

    print("Starting document chunking...")

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ".", " ", ""]
    )

    chunks = text_splitter.split_documents(documents)

    print(f"Total chunks created: {len(chunks)}")

    # preview some chunks
    for i, chunk in enumerate(chunks[:3]):
        print(f"\nChunk {i+1}")
        print("Source:", chunk.metadata)
        print("Length:", len(chunk.page_content))
        print("Content preview:", chunk.page_content[:150])

    return chunks
def main():
    print("Starting to load HuggingFace datasets...")
    documents = load_all_datasets()
    print("Chunking documents...")
    chunks = split_documents(documents)
    return chunks



if __name__ == "__main__":
    main() 