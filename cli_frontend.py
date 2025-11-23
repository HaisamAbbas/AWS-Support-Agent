"""
CLI-based frontend for the AWS Support Agent.
Allows users to ask questions about AWS and get answers using the created agent.
"""

import os
import sys
from typing import Tuple
from steps.url_scraper import url_scraper
from steps.web_url_loader import web_url_loader
from steps.index_generator import index_generator
from steps.agent_creator import aws_agent_creator, AgentParameters

def create_aws_agent():
    """
    Create the AWS Support Agent with sample data for immediate use.
    """
    print("[INFO] Creating AWS Support Agent...")
    
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
        ),
        Document(
            page_content="AWS Lambda is a serverless compute service that runs your code in response to events and automatically manages the underlying compute resources for you. You can use Lambda to extend other AWS services with custom logic, or create your own back-end services.",
            metadata={"source": "lambda_documentation"}
        ),
        Document(
            page_content="AWS IAM (Identity and Access Management) enables you to manage access to AWS services and resources securely. Using IAM, you can create and manage AWS users and groups, and use permissions to allow and deny their access to AWS resources.",
            metadata={"source": "iam_documentation"}
        ),
        Document(
            page_content="AWS CloudFormation provides a common language for describing and provisioning AWS infrastructure. You can use CloudFormation to describe your entire AWS infrastructure and have it created and managed in an automated and secure way.",
            metadata={"source": "cloudformation_documentation"}
        )
    ]
    
    print(f"[INFO] Created {len(documents)} sample documents")
    
    print("[INFO] Creating vector store...")
    vector_store = index_generator(documents)
    print("[INFO] Vector store created successfully")
    
    print("[INFO] Creating AWS Support Agent with GROQ...")
    
    config = AgentParameters(
        llm_type="groq",  
        groq_model_name="llama-3.1-8b-instant",  
        temperature=0.2,
        max_tokens=1200
    )
    
    agent, tools, executor = aws_agent_creator(vector_store=vector_store, config=config)
    print("[SUCCESS] AWS Support Agent created successfully!")
    
    return agent, tools, executor, vector_store

def main():
    """
    Main CLI loop for interacting with the AWS Support Agent.
    """
    print("=" * 60)
    print("AWS Support Agent - CLI Interface")
    print("=" * 60)
    print("Ask questions about AWS services, configurations, and best practices.")
    print("Type 'quit', 'exit', or 'q' to exit the application.")
    print("Type 'help' for assistance.")
    print("-" * 60)
    
    if not os.getenv("GROQ_API_KEY"):
        raise ValueError("GROQ_API_KEY environment variable is required")
    
    try:
        agent, tools, executor, vector_store = create_aws_agent()
        print("\n[READY] AWS Support Agent is ready to answer your questions!")
        print("Example: 'What is AWS EC2?' or 'How do I create an S3 bucket?'")
    except Exception as e:
        print(f"[ERROR] Failed to create agent: {e}")
        print("Please make sure all dependencies are installed and your API key is correct.")
        sys.exit(1)
    
    while True:
        try:
            user_input = input("\nYou: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("\nThank you for using the AWS Support Agent. Goodbye!")
                break
            elif user_input.lower() in ['help', 'info', '?']:
                print("\nAWS Support Agent Help:")
                print("  - Ask questions about AWS services (EC2, S3, Lambda, etc.)")
                print("  - Ask about AWS configurations and best practices")
                print("  - Ask about AWS security and IAM")
                print("  - Type 'quit' or 'exit' to leave")
                continue
            elif not user_input:
                print("Please enter a question.")
                continue
            
            print("AWS Agent: ", end="", flush=True)
            
            try:
                response = executor.invoke({"input": user_input})
                if isinstance(response, dict) and "output" in response:
                    print(response["output"])
                else:
                    print(str(response))
            except Exception as e:
                print(f"[ERROR] Failed to process query: {e}")
                print("Please try rephrasing your question.")
                
        except KeyboardInterrupt:
            print("\n\nThank you for using the AWS Support Agent. Goodbye!")
            break
        except EOFError:
            print("\n\nThank you for using the AWS Support Agent. Goodbye!")
            break

if __name__ == "__main__":
    main()