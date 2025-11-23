import os
from typing import List

import nltk
from langchain_community.docstore.document import Document
from langchain_community.document_loaders import UnstructuredURLLoader


def web_url_loader(urls: List[str]) -> List[Document]:
    """Loads documents from a list of AWS-related URLs.

    Args:
        urls: List of URLs to load documents from (produced by url_scraper).

    Returns:
        List of LangChain Document objects.
    """
    nltk_data_dir = os.path.join(os.getcwd(), "nltk_data")
    os.makedirs(nltk_data_dir, exist_ok=True)
    nltk.data.path.append(nltk_data_dir)

    nltk.download("punkt", download_dir=nltk_data_dir, quiet=True)
    nltk.download("wordnet", download_dir=nltk_data_dir, quiet=True)
    nltk.download("omw-1.4", download_dir=nltk_data_dir, quiet=True)
    nltk.download("punkt_tab", download_dir=nltk_data_dir, quiet=True)
    nltk.download("averaged_perceptron_tagger_eng", download_dir=nltk_data_dir, quiet=True)

    loader = UnstructuredURLLoader(urls=urls)
    try:
        docs = loader.load()
        print(f"[INFO] Loaded {len(docs)} AWS documents.")
    except Exception as e:
        print(f"[ERROR] URL loading failed: {e}")
        docs = []

    return docs
