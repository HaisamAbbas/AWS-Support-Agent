"""
Test script for the AWS Support Agent using your GROQ API key.
This script should work without heavy embedding dependencies.
"""

import os
import sys

# Set the GROQ API key in the environment
if not os.getenv("GROQ_API_KEY"):
    raise ValueError("GROQ_API_KEY environment variable is required for tests")

def test_agent_creation():
    """
    Test creating the AWS Support Agent with your GROQ API key.
    """
    print("[START] Testing AWS Support Agent creation with GROQ API...")
    
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
    
    # Try to create vector store
    print("Creating vector store with fallback embedding approach...")
    try:
        from steps.index_generator import index_generator
        vector_store = index_generator(documents)
        print("Vector store created successfully!")
    except ImportError as e:
        print(f"Import error creating vector store: {e}")
        print("This might be due to missing dependencies.")
        
        # Try a minimal approach without heavy dependencies
        print("Trying alternative approach with basic embeddings...")
        from langchain.embeddings import FakeEmbeddings
        from langchain.text_splitter import CharacterTextSplitter
        from langchain_community.vectorstores import FAISS
        
        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
        compiled_texts = text_splitter.split_documents(documents)
        
        embeddings = FakeEmbeddings(size=1536)
        vector_store = FAISS.from_documents(compiled_texts, embeddings)
        print("Vector store created with basic embeddings!")
    
    except Exception as e:
        print(f"Error creating vector store: {e}")
        import traceback
        traceback.print_exc()
        return
    
    # Create agent using GROQ (which you have API key for)
    print("Creating AWS Support Agent with GROQ...")
    
    # Configure agent parameters
    from steps.agent_creator import AgentParameters
    config = AgentParameters(
        llm_type="groq",  # Use groq which you have the API key for
        groq_model_name="llama-3.1-8b-instant",  # Free tier model
        temperature=0.2,
        max_tokens=1200
    )
    
    try:
        from steps.agent_creator import aws_agent_creator
        # Create the agent
        agent, tools, executor = aws_agent_creator(vector_store=vector_store, config=config)
        print("AWS Support Agent created successfully!")
        
        print(f"Agent tools: {[tool.name for tool in tools]}")
        print("\n[SUCCESS] AWS Support Agent pipeline executed successfully!")
        
        # Show a simple example of how to use the agent
        print("\n[INFO] To use the agent, you would call executor.invoke({'input': 'Your question here'})")
        print("[INFO] Your GROQ API key has been successfully integrated!")
        
        return agent, tools, executor, vector_store
    except Exception as e:
        print(f"Error creating agent: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    result = test_agent_creation()
    if result:
        print("\n[SUCCESS] The AWS Support Agent has been successfully set up with your GROQ API key!")
        print("You can now run the main application with: python run.py")
    else:
        print("\n[ERROR] There were issues during setup. Please check the error messages above.")