from steps.agent_creator import aws_agent_creator as agent_creator
from steps.index_generator import index_generator
from steps.url_scraper import url_scraper
from steps.web_url_loader import web_url_loader


def aws_agent_creation_pipeline():
    """Generate vector index for AWS Cloud documentation and repositories.

    This pipeline:
    1. Scrapes AWS documentation, website, and GitHub samples.
    2. Loads the content into LangChain documents.
    3. Generates vector embeddings and builds a FAISS index.
    4. Creates an AWS Agent capable of answering cloud-related questions.
    """
    urls = url_scraper()
    documents = web_url_loader(urls)
    vector_store = index_generator(documents)
    _ = agent_creator(vector_store=vector_store)
    return vector_store


if __name__ == "__main__":
    vector_store = aws_agent_creation_pipeline()