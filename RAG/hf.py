from datasets import load_dataset
from langchain_core.documents import Document

def load_hf_dataset(dataset_name, max_rows=2000):

    print(f"Loading dataset: {dataset_name}")

    ds = load_dataset(dataset_name)

    documents = []

    count = 0

    for row in ds["train"]:

        text = " ".join([str(v) for v in row.values()])

        documents.append(
            Document(
                page_content=text,
                metadata={"source": dataset_name}
            )
        )

        count += 1

        if count >= max_rows:
            break

    print(f"{dataset_name} → {len(documents)} records loaded")

    return documents

def load_hr_huggingface_datasets():

    datasets_list = [
        "EmbraceCoder/HR_Policy",
        "Synkro123/hr-policy-traces",
        "syncora/hr-policies-qa-dataset",
        "saunak14/sample_employee_dataset",
        "SRIHARSHATA/employees",
        "Farica10/Employee_attributes",
        "kmrmanish/Employees_Reviews_Dataset"
    ]

    documents = []

    for dataset in datasets_list:

        try:
            docs = load_hf_dataset(dataset, max_rows=1500)
            documents.extend(docs)

        except Exception as e:
            print(f"Skipping {dataset}: {e}")

    print(f"\nTotal HuggingFace documents loaded: {len(documents)}")

    return documents

def main():
    print("Starting to load HuggingFace datasets...")


if __name__ == "__main__":
    main()