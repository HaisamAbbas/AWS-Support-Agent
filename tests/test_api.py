"""
Example script to test the AWS Support Agent API
Run this after starting the API server with: python api_run.py
"""
import requests
import json
import time

# Base URL for the API
BASE_URL = "http://localhost:8000"


def print_section(title):
    """Print a formatted section header."""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def print_response(response):
    """Pretty print the JSON response."""
    print(json.dumps(response.json(), indent=2))


def main():
    """Main function to test the API endpoints."""
    
    print_section("AWS Support Agent API Test")
    print("Testing all API endpoints...")
    print("Make sure the API server is running on http://localhost:8000")
    
    try:
        # 1. Health Check
        print_section("1. Health Check - GET /health")
        response = requests.get(f"{BASE_URL}/health")
        print(f"Status Code: {response.status_code}")
        print_response(response)
        
        # 2. Check Agent Status (Before Initialization)
        print_section("2. Agent Status - GET /agent/status (Before Init)")
        response = requests.get(f"{BASE_URL}/agent/status")
        print(f"Status Code: {response.status_code}")
        print_response(response)
        
        # 3. Initialize Agent
        print_section("3. Initialize Agent - POST /agent/initialize")
        print("Initializing agent... This may take a few seconds...")
        response = requests.post(f"{BASE_URL}/agent/initialize")
        print(f"Status Code: {response.status_code}")
        print_response(response)
        
        # 4. Check Agent Status (After Initialization)
        print_section("4. Agent Status - GET /agent/status (After Init)")
        response = requests.get(f"{BASE_URL}/agent/status")
        print(f"Status Code: {response.status_code}")
        print_response(response)
        
        # 5. Get Agent Configuration
        print_section("5. Agent Configuration - GET /agent/config")
        response = requests.get(f"{BASE_URL}/agent/config")
        print(f"Status Code: {response.status_code}")
        print_response(response)
        
        # 6. Query Agent - Simple Question
        print_section("6. Query Agent - POST /agent/query (Simple)")
        query_data = {
            "query": "What is AWS EC2?",
            "include_sources": False
        }
        print(f"Question: {query_data['query']}")
        response = requests.post(f"{BASE_URL}/agent/query", json=query_data)
        print(f"Status Code: {response.status_code}")
        print_response(response)
        
        # 7. Query Agent - With Sources
        print_section("7. Query Agent - POST /agent/query (With Sources)")
        query_data = {
            "query": "How does AWS S3 work?",
            "include_sources": True
        }
        print(f"Question: {query_data['query']}")
        response = requests.post(f"{BASE_URL}/agent/query", json=query_data)
        print(f"Status Code: {response.status_code}")
        print_response(response)
        
        # 8. Query Agent - Complex Question
        print_section("8. Query Agent - Complex Question")
        query_data = {
            "query": "What are the differences between AWS Lambda and EC2?",
            "include_sources": False
        }
        print(f"Question: {query_data['query']}")
        response = requests.post(f"{BASE_URL}/agent/query", json=query_data)
        print(f"Status Code: {response.status_code}")
        print_response(response)
        
        # 9. Final Status Check
        print_section("9. Final Agent Status - GET /agent/status")
        response = requests.get(f"{BASE_URL}/agent/status")
        print(f"Status Code: {response.status_code}")
        print_response(response)
        
        print_section("✅ All Tests Completed Successfully!")
        print("The API is working correctly and ready for frontend integration.")
        
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Could not connect to the API server.")
        print("Please make sure the server is running:")
        print("   python api_run.py")
        return
    
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        return


if __name__ == "__main__":
    main()
