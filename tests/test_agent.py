import os
from langchain.schema.document import Document
from steps.agent_creator import AgentParameters, aws_agent_creator

# Ensure Groq API key is set
if not os.getenv('GROQ_API_KEY'):
    raise ValueError("GROQ_API_KEY environment variable is required for tests")

# Create a simple configuration for Groq
config = AgentParameters(
    llm_type="groq",
    groq_api_key=os.getenv('GROQ_API_KEY'),
    groq_model_name="llama3-8b-8192",
    temperature=0.2,
    max_tokens=1200
)

# Create a mock vector store (we'll create a simple one for testing)
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

# Create some sample documents
documents = [Document(page_content="AWS S3 is a storage service", metadata={"source": "test"})]

# Create embeddings
embeddings = OpenAIEmbeddings()

# Create a simple FAISS vector store
vector_store = FAISS.from_documents(documents, embeddings)

try:
    # Create the AWS agent
    agent, tools = aws_agent_creator(vector_store=vector_store, config=config)
    print("Successfully created AWS Support Agent with Groq!")
    print(f"Using LLM type: {config.llm_type}")
    print(f"Model: {config.groq_model_name}")
    print(f"Number of tools: {len(tools)}")
    print("The agent is ready to use with your Groq API key!")
except Exception as e:
    print(f"Error creating agent: {e}")
    import traceback
    traceback.print_exc()