try:
    from .hf import load_hr_huggingface_datasets
    from .kaggle import load_kaggle_datasets
except ImportError:
    # If relative imports fail (e.g. when run directly), fall back to absolute imports
    from hf import load_hr_huggingface_datasets
    from kaggle import load_kaggle_datasets


def load_all_datasets():

    print("Loading all HR datasets...\n")

    hf_docs = load_hr_huggingface_datasets()

    kaggle_docs = load_kaggle_datasets()

    documents = hf_docs + kaggle_docs

    print(f"\nTotal documents loaded: {len(documents)}")

    return documents

def main():
    documents = load_all_datasets()


if __name__ == "__main__":
    main()