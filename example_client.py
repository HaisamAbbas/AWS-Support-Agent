"""
Simple Python Client for AWS Support Agent API
This module provides a clean interface to interact with the API
"""
import requests
from typing import Optional, Dict, Any


class AWSAgentClient:
    """Client class for interacting with AWS Support Agent API."""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        """
        Initialize the client.
        
        Args:
            base_url: Base URL of the API server
        """
        self.base_url = base_url.rstrip('/')
        self._initialized = False
    
    def health_check(self) -> Dict[str, Any]:
        """
        Check API health status.
        
        Returns:
            Health status information
        """
        response = requests.get(f"{self.base_url}/health")
        response.raise_for_status()
        return response.json()
    
    def initialize(self, force_reinit: bool = False) -> Dict[str, Any]:
        """
        Initialize the agent.
        
        Args:
            force_reinit: Force re-initialization
            
        Returns:
            Initialization status
        """
        response = requests.post(
            f"{self.base_url}/agent/initialize",
            params={"force_reinit": force_reinit}
        )
        response.raise_for_status()
        self._initialized = True
        return response.json()
    
    def get_status(self) -> Dict[str, Any]:
        """
        Get agent status.
        
        Returns:
            Agent status information
        """
        response = requests.get(f"{self.base_url}/agent/status")
        response.raise_for_status()
        return response.json()
    
    def get_config(self) -> Dict[str, Any]:
        """
        Get agent configuration.
        
        Returns:
            Agent configuration
        """
        response = requests.get(f"{self.base_url}/agent/config")
        response.raise_for_status()
        return response.json()
    
    def query(
        self, 
        question: str, 
        include_sources: bool = False
    ) -> Dict[str, Any]:
        """
        Query the AWS Support Agent.
        
        Args:
            question: Your question about AWS
            include_sources: Include source documents in response
            
        Returns:
            Agent response with metadata
        """
        if not self._initialized:
            print("⚠️  Agent not initialized. Initializing now...")
            self.initialize()
        
        response = requests.post(
            f"{self.base_url}/agent/query",
            json={
                "query": question,
                "include_sources": include_sources
            }
        )
        response.raise_for_status()
        return response.json()
    
    def ask(self, question: str) -> str:
        """
        Simple method to ask a question and get just the answer text.
        
        Args:
            question: Your question about AWS
            
        Returns:
            Agent's answer as string
        """
        result = self.query(question)
        return result.get("response", "")


# Example usage
if __name__ == "__main__":
    # Create client
    client = AWSAgentClient()
    
    print("=" * 70)
    print("AWS Support Agent - Python Client Example")
    print("=" * 70)
    
    # Check health
    print("\n1. Checking API health...")
    health = client.health_check()
    print(f"   Status: {health['status']}")
    
    # Initialize agent
    print("\n2. Initializing agent...")
    init_result = client.initialize()
    print(f"   {init_result['message']}")
    
    # Check status
    print("\n3. Checking agent status...")
    status = client.get_status()
    print(f"   Initialized: {status['initialized']}")
    print(f"   LLM: {status['llm_type']} ({status['model_name']})")
    
    # Ask questions
    print("\n4. Asking questions...")
    
    questions = [
        "What is AWS EC2?",
        "How do I create an S3 bucket?",
        "What's the difference between Lambda and EC2?"
    ]
    
    for i, question in enumerate(questions, 1):
        print(f"\n   Question {i}: {question}")
        answer = client.ask(question)
        print(f"   Answer: {answer[:200]}...")  # Print first 200 chars
    
    # Get final status
    print("\n5. Final status...")
    status = client.get_status()
    print(f"   Total queries processed: {status['total_queries']}")
    
    print("\n" + "=" * 70)
    print("✅ Example completed successfully!")
    print("=" * 70)
