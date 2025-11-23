"""
Direct test runner for the AWS Support Agent without ZenML dependencies.
This file runs the agent creation pipeline directly.
"""

import os
from steps.web_url_loader import web_url_loader
from steps.index_generator import index_generator
from steps.agent_creator import aws_agent_creator, AgentParameters

def run_aws_agent_pipeline():
    """
    Run the AWS Support Agent pipeline directly without ZenML.
    """
    print("[START] Starting AWS Support Agent pipeline...")
    
    # Define a small set of URLs to avoid extensive crawling
    test_urls = [
        "https://aws.amazon.com/",
        "https://docs.aws.amazon.com/"
    ]
    
    print(f"Using test URLs: {test_urls}")
    
    # Load documents from URLs
    print("Loading documents from URLs...")
    try:
        documents = web_url_loader(test_urls)
    except Exception as e:
        print(f"Error loading documents: {e}")
        documents = []
    
    if not documents:
        print("No documents loaded, using sample data...")
        # Create a simple document for testing
        from langchain_community.docstore.document import Document
        documents = [
            Document(
                page_content="AWS provides cloud computing services that help businesses scale and grow. "
                             "AWS services include EC2 for compute, S3 for storage, and Lambda for serverless computing.",
                metadata={"source": "aws_basics"}
            )
        ]
    
    print(f"Loaded {len(documents)} documents")
    
    # Create vector store
    print("Creating vector store...")
    try:
        vector_store = index_generator(documents)
        print("Vector store created successfully")
    except Exception as e:
        print(f"Error creating vector store: {e}")
        return
    
    # Create agent
    print("Creating AWS Support Agent...")
    
    # Configure agent parameters - using GROQ since it's available
    config = AgentParameters(
        llm_type="groq",  # Use groq which you have the API key for
        groq_model_name="llama-3.1-8b-instant",  # Free tier model
        temperature=0.2,
        max_tokens=1200,
        groq_api_key=os.getenv("GROQ_API_KEY")
    )
    
    try:
        # Create the agent
        agent, tools, executor = aws_agent_creator(vector_store=vector_store, config=config)
        print("AWS Support Agent created successfully")
        
        return agent, tools, executor, vector_store
    except Exception as e:
        print(f"Error creating agent: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    try:
        result = run_aws_agent_pipeline()
        if result:
            agent, tools, executor, vector_store = result
            print("\n[SUCCESS] AWS Support Agent pipeline executed successfully!")
            print(f"Agent tools: {[tool.name for tool in tools]}")
        
    except Exception as e:
        print(f"[ERROR] Pipeline execution failed: {e}")
        import traceback
        traceback.print_exc()