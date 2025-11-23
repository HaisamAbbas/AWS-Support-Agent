import os
from typing import Dict, List, Tuple, Literal

from agent.prompt import PREFIX, SUFFIX
from langchain.agents import AgentExecutor, ConversationalChatAgent
from langchain.schema.vectorstore import VectorStore
from langchain.tools.base import BaseTool
from langchain_community.tools.vectorstore.tool import VectorStoreQATool
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
from langchain_groq import ChatGroq
from pydantic import BaseModel

PIPELINE_NAME = "aws_support_agent_pipeline"
CHARACTER = "AWS cloud support specialist"

class AgentParameters(BaseModel):
    """Parameters for the AWS Support Agent."""
    
 
    llm_type: Literal["openai", "ollama", "groq"] = "groq"  # Changed to groq by default to use your API key
    
    
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    openai_model_name: str = "gpt-4o-mini"
    
    
    ollama_model_name: str = "llama3.2"  # Default model, can be changed
    
    
    groq_api_key: str = os.getenv("GROQ_API_KEY", "")
    groq_model_name: str = "llama-3.1-8b-instant"  # Default Groq model (free tier)
    
    
    temperature: float = 0.2
    max_tokens: int = 1200

    class Config:
        extra = "ignore"


def get_llm_instance(config: AgentParameters):
    """Return the appropriate LLM instance based on configuration."""
    if config.llm_type == "openai":
        api_key = config.openai_api_key or os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError(
                "No OpenAI API key found. Please set the OPENAI_API_KEY environment variable."
            )
        
        return ChatOpenAI(
            model_name=config.openai_model_name,
            temperature=config.temperature,
            max_tokens=config.max_tokens,
            api_key=api_key
        )
    elif config.llm_type == "ollama":
        return ChatOllama(
            model=config.ollama_model_name,
            temperature=config.temperature,
            num_predict=config.max_tokens,
            base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        )
    elif config.llm_type == "groq":
        api_key = config.groq_api_key or os.getenv("GROQ_API_KEY")
        
        if not api_key:
            raise ValueError(
                "No Groq API key found. Please set the GROQ_API_KEY environment variable, or "
                "get a free API key from: https://console.groq.com/keys"
            )
        
        return ChatGroq(
            model=config.groq_model_name,
            temperature=config.temperature,
            max_tokens=config.max_tokens,
            api_key=api_key
        )
    else:
        raise ValueError(f"Unsupported LLM type: {config.llm_type}")


def aws_agent_creator(
    vector_store: VectorStore, config: AgentParameters = AgentParameters()
):
    """Create an AWS Support Agent from a vector store.

    Args:
        vector_store: The AWS knowledge base (vector store) to create the agent from.
        config: Configuration parameters for the agent, including LLM settings.

    Returns:
        A tuple containing the conversational agent and its tools.
    """
    llm = get_llm_instance(config)
    
    tools = [
        VectorStoreQATool(
            name="aws-support-qa-tool",
            vectorstore=vector_store,
            description=(
                "Use this tool to answer questions about AWS services, troubleshooting, "
                "deployment errors, configuration issues, and service best practices. "
                "Covers S3, EC2, Lambda, IAM, CloudWatch, and general AWS documentation."
            ),
            llm=llm,
        ),
    ]

    from langchain.agents import ConversationalChatAgent, AgentExecutor
    from langchain.memory import ConversationBufferMemory
    from langchain.prompts import MessagesPlaceholder
    from langchain.schema import SystemMessage
    
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    
    # Create custom conversational agent with AWS system prompt
    system_message = SystemMessage(content=PREFIX)
    
    agent = ConversationalChatAgent.from_llm_and_tools(
        llm=llm,
        tools=tools,
        system_message=system_message.content,
        verbose=True,
    )
    
    executor = AgentExecutor.from_agent_and_tools(
        agent=agent,
        tools=tools,
        memory=memory,
        verbose=True,
        handle_parsing_errors=True,
    )

    
    print(f"Created AWS Support Agent with tools: {[tool.name for tool in tools]}")
    print(f"Using LLM type: {config.llm_type}")
    print(f"Model name: {config.ollama_model_name if config.llm_type == 'ollama' else config.groq_model_name if config.llm_type == 'groq' else config.openai_model_name}")
    print(f"System prompt: {PREFIX[:100]}...")

    return None, tools, executor  