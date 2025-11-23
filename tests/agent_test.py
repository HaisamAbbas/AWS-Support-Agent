"""
Quick test to verify the AWS Support Agent functionality with GROQ API integration.
"""

import os
from steps.agent_creator import AgentParameters, aws_agent_creator
from steps.index_generator import index_generator

def test_agent_query():
    """
    Test the agent with a simple query to verify it works.
    """
    print("Testing AWS Support Agent with sample query...")
    
    # Set the GROQ API key
    if not os.getenv("GROQ_API_KEY"):
        raise ValueError("GROQ_API_KEY environment variable is required for tests")
    
    # Create sample documents for testing
    from langchain_community.docstore.document import Document
    documents = [
        Document(
            page_content="Amazon EC2 (Elastic Compute Cloud) provides scalable computing capacity in the AWS cloud. You can use EC2 to launch virtual servers, known as instances, and manage them according to your application needs. EC2 instances can be configured with various operating systems, CPU, memory, storage, and networking capacity.",
            metadata={"source": "ec2_basics"}
        ),
        Document(
            page_content="AWS S3 (Simple Storage Service) is object storage built to store and retrieve any amount of data from anywhere on the web. It's a simple web services interface for storing and retrieving any amount of data at any time. S3 has management features to optimize costs, apply security and compliance controls, and monitor configuration changes.",
            metadata={"source": "s3_basics"}
        )
    ]
    
    # Create the vector store
    vector_store = index_generator(documents)
    
    # Configure agent parameters to use GROQ
    config = AgentParameters(
        llm_type="groq",  # Use groq which you have the API key for
        groq_model_name="llama-3.1-8b-instant",  # Free tier model
        temperature=0.2,
        max_tokens=1200
    )
    
    # Create the agent
    agent, tools, executor = aws_agent_creator(vector_store=vector_store, config=config)
    
    # Test with a simple query
    test_query = "What is AWS EC2?"
    
    print(f"\nQuery: {test_query}")
    try:
        response = executor.invoke({"input": test_query})
        if isinstance(response, dict) and "output" in response:
            print(f"Response: {response['output']}")
        else:
            print(f"Response: {response}")
    except Exception as e:
        print(f"Error during query: {e}")
    
    print("\nAgent test completed successfully!")
    return executor

if __name__ == "__main__":
    executor = test_agent_query()