import kagglehub
import pandas as pd
import os
from langchain_core.documents import Document


def load_kaggle_dataset(dataset_name, sample_size=2000):

    print(f"Downloading Kaggle dataset: {dataset_name}")

    path = kagglehub.dataset_download(dataset_name)

    documents = []

    for file in os.listdir(path):

        if file.endswith(".csv"):

            df = pd.read_csv(os.path.join(path, file))

            df = df.sample(min(sample_size, len(df)))

            for _, row in df.iterrows():

                text = " ".join([str(v) for v in row.values])

                documents.append(
                    Document(
                        page_content=text,
                        metadata={"source": dataset_name}
                    )
                )

    print(f"{dataset_name} → {len(documents)} records loaded")

    return documents

def load_kaggle_datasets():

    kaggle_list = [
        "rhuebner/human-resources-data-set",
        "ravindrasinghrana/employeedataset"
    ]

    documents = []

    for dataset in kaggle_list:

        docs = load_kaggle_dataset(dataset)
        documents.extend(docs)

    print(f"Total Kaggle documents: {len(documents)}")

    return documents

def main():
    print("Starting to load HuggingFace datasets...")


if __name__ == "__main__":
    main()