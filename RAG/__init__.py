"""RAG package initializer.

This allows modules under the RAG directory to be imported as a package
(e.g. ``from RAG import hf``).
"""

from .hf import load_hr_huggingface_datasets
from .kaggle import load_kaggle_datasets
from .bothdataset import load_all_datasets
from .chunking import split_documents
from .embedding import create_vector_store
