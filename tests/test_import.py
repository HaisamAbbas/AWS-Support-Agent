try:
    from langchain_huggingface import HuggingFaceEmbeddings
    print("Successfully imported HuggingFaceEmbeddings from langchain_huggingface")
except ImportError:
    print("Failed to import from langchain_huggingface")

    try:
        from langchain_community.embeddings import HuggingFaceEmbeddings
        print("Successfully imported HuggingFaceEmbeddings from langchain_community.embeddings")
    except ImportError:
        print("Failed to import from langchain_community.embeddings")

        try:
            from langchain.embeddings import HuggingFaceEmbeddings
            print("Successfully imported HuggingFaceEmbeddings from langchain.embeddings")
        except ImportError:
            print("Failed to import from langchain.embeddings")