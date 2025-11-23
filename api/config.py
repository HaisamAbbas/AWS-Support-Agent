"""
Configuration management for the FastAPI application.
"""
import os
from typing import Literal
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings and environment variables."""
    
    # API Configuration
    app_name: str = "AWS Support Agent API"
    app_version: str = "1.0.0"
    app_description: str = "FastAPI backend for AWS Support Agent powered by LangChain and GROQ"
    debug: bool = False
    
    # CORS Configuration
    cors_origins: list = ["*"]
    cors_credentials: bool = True
    cors_methods: list = ["*"]
    cors_headers: list = ["*"]
    
    # LLM Configuration
    llm_type: Literal["openai", "ollama", "groq"] = "groq"
    groq_api_key: str = os.getenv("GROQ_API_KEY", "")
    groq_model_name: str = "llama-3.1-8b-instant"
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    openai_model_name: str = "gpt-4o-mini"
    ollama_model_name: str = "llama3.2"
    ollama_base_url: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    
    # Agent Configuration
    temperature: float = 0.2
    max_tokens: int = 1200
    
    # AWS Configuration (if needed)
    aws_region: str = os.getenv("AWS_REGION", "us-east-1")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


# Global settings instance
settings = Settings()
