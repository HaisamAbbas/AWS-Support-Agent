import os
from langchain_community.vectorstores.faiss import FAISS


def save_vector_store(data: FAISS, path: str) -> None:
    """Save the FAISS index and documents.

    Args:
        data: The FAISS vector store to save
        path: Path to save the vector store to
    """
    data.save_local(path)


def load_vector_store(path: str) -> FAISS:
    """Load the FAISS index and documents.

    Args:
        path: Path to load the vector store from

    Returns:
        The loaded FAISS vector store
    """
    if os.getenv("OPENAI_API_KEY"):
        from langchain_openai import OpenAIEmbeddings
        embeddings = OpenAIEmbeddings()
    else:
        try:
            from langchain_community.embeddings import HuggingFaceEmbeddings
            embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        except ImportError:
            from langchain_community.embeddings import FakeEmbeddings
            embeddings = FakeEmbeddings(size=1536)  
    
    return FAISS.load_local(
        path,
        embeddings=embeddings,
        allow_dangerous_deserialization=True,
    )
