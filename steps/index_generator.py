import os
from typing import List
from langchain.schema.vectorstore import VectorStore
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.docstore.document import Document
from langchain_community.vectorstores import FAISS

def index_generator(
    documents: List[Document],
):

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
    
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    compiled_texts = text_splitter.split_documents(documents)

    print(f"Created vector store with {len(compiled_texts)} text chunks using embedding approach")

    vector_store = FAISS.from_documents(
        compiled_texts,
        embeddings
    )

    return vector_store
