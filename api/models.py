"""
Pydantic models for request/response validation.
"""
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime


class HealthResponse(BaseModel):
    """Health check response model."""
    status: str = Field(..., description="API health status")
    version: str = Field(..., description="API version")
    timestamp: str = Field(..., description="Current timestamp")


class AgentStatusResponse(BaseModel):
    """Agent status response model."""
    initialized: bool = Field(..., description="Whether the agent is initialized")
    llm_type: str = Field(..., description="Type of LLM being used")
    model_name: str = Field(..., description="Name of the model")
    total_queries: int = Field(default=0, description="Total number of queries processed")


class QueryRequest(BaseModel):
    """Request model for querying the agent."""
    query: str = Field(..., min_length=1, max_length=2000, description="User query about AWS")
    include_sources: bool = Field(default=False, description="Include source documents in response")
    
    class Config:
        json_schema_extra = {
            "example": {
                "query": "What is AWS EC2?",
                "include_sources": False
            }
        }


class QueryResponse(BaseModel):
    """Response model for agent queries."""
    query: str = Field(..., description="Original user query")
    response: str = Field(..., description="Agent's response")
    sources: Optional[List[str]] = Field(default=None, description="Source documents used")
    processing_time: float = Field(..., description="Time taken to process query (seconds)")
    timestamp: str = Field(..., description="Timestamp of the response")
    
    class Config:
        json_schema_extra = {
            "example": {
                "query": "What is AWS EC2?",
                "response": "AWS EC2 (Elastic Compute Cloud) provides scalable computing capacity...",
                "sources": ["ec2_documentation"],
                "processing_time": 1.23,
                "timestamp": "2025-11-22T10:30:00"
            }
        }


class ErrorResponse(BaseModel):
    """Error response model."""
    error: str = Field(..., description="Error type")
    message: str = Field(..., description="Error message")
    detail: Optional[str] = Field(default=None, description="Additional error details")
    timestamp: str = Field(..., description="Error timestamp")


class ConfigResponse(BaseModel):
    """Configuration response model."""
    llm_type: str = Field(..., description="LLM type being used")
    model_name: str = Field(..., description="Model name")
    temperature: float = Field(..., description="Temperature setting")
    max_tokens: int = Field(..., description="Max tokens setting")
