"""
Simple test to check if we can create an AWS Support Agent without ZenML.
This tests the core functionality without URL scraping.
"""

import os
from steps.index_generator import index_generator
from steps.agent_creator import aws_agent_creator, AgentParameters

def test_agent_creation():
    """
    Test creating the AWS Support Agent with minimal dependencies.
    """
    print("[START] Testing AWS Support Agent creation...")
    
    # Create sample documents directly
    from langchain_community.docstore.document import Document
    documents = [
        Document(
            page_content="Amazon Web Services (AWS) is a comprehensive cloud platform offering over 200 fully-featured services from data centers globally. AWS services include EC2 for compute, S3 for storage, Lambda for serverless computing, RDS for databases, and many more.",
            metadata={"source": "aws_overview"}
        ),
        Document(
            page_content="AWS EC2 (Elastic Compute Cloud) provides scalable computing capacity in the AWS cloud. You can use EC2 to launch virtual servers, known as instances, and manage them according to your application needs.",
            metadata={"source": "ec2_documentation"}
        ),
        Document(
            page_content="AWS S3 (Simple Storage Service) is object storage built to store and retrieve any amount of data from anywhere on the web. It's a simple web services interface for storing and retrieving any amount of data at any time.",
            metadata={"source": "s3_documentation"}
        )
    ]
    
    print(f"Created {len(documents)} sample documents")
    
    # Create vector store
    print("Creating vector store with HuggingFace embeddings...")
    try:
        vector_store = index_generator(documents)
        print("Vector store created successfully")
    except Exception as e:
        print(f"Error creating vector store: {e}")
        import traceback
        traceback.print_exc()
        return
    
    # Create agent using GROQ (which you have API key for)
    print("Creating AWS Support Agent with GROQ...")
    
    # Configure agent parameters
    config = AgentParameters(
        llm_type="groq",  # Use groq which you have the API key for
        groq_model_name="llama-3.1-8b-instant",  # Free tier model
        temperature=0.2,
        max_tokens=1200
    )
    
    # Set the GROQ API key in the environment for the agent creator
    if not os.getenv("GROQ_API_KEY"):
        raise ValueError("GROQ_API_KEY environment variable is required for tests")
    
    try:
        # Create the agent
        agent, tools, executor = aws_agent_creator(vector_store=vector_store, config=config)
        print("AWS Support Agent created successfully!")
        
        print(f"Agent tools: {[tool.name for tool in tools]}")
        print("\n[SUCCESS] AWS Support Agent pipeline executed successfully!")
        
        # Show a simple example of how to use the agent
        print("\n[INFO] To use the agent, you would call executor.invoke({'input': 'Your question here'})")
        
        return agent, tools, executor, vector_store
    except Exception as e:
        print(f"Error creating agent: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    result = test_agent_creation()