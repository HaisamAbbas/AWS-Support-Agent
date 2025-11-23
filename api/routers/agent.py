"""
Agent API Router
Handles all agent-related endpoints including queries, status, and configuration.
"""
from fastapi import APIRouter, HTTPException, status, Depends
from datetime import datetime

from api.models import (
    QueryRequest,
    QueryResponse,
    AgentStatusResponse,
    ConfigResponse,
    ErrorResponse
)
from api.agent_service import agent_service
from api.auth import validate_api_key

router = APIRouter(
    prefix="/agent",
    tags=["agent"],
    responses={
        500: {"model": ErrorResponse, "description": "Internal Server Error"},
        503: {"model": ErrorResponse, "description": "Service Unavailable"}
    }
)


@router.post(
    "/query",
    response_model=QueryResponse,
    status_code=status.HTTP_200_OK,
    summary="Query the AWS Support Agent",
    description="Send a query to the AWS Support Agent and get a response based on AWS documentation and knowledge base."
)
async def query_agent(request: QueryRequest, user: dict = Depends(validate_api_key)):
    """
    Query the AWS Support Agent with a question about AWS services.
    
    - **query**: Your question about AWS (required, 1-2000 characters)
    - **include_sources**: Whether to include source documents in the response (optional)
    
    Returns the agent's response along with metadata like processing time and timestamp.
    
    Requires authentication via Bearer token.
    """
    try:
        # Ensure agent is initialized
        if not agent_service.get_status()["initialized"]:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Agent not initialized. Please call /agent/initialize first."
            )
        
        # Process query
        result = agent_service.query_agent(
            query=request.query,
            include_sources=request.include_sources
        )
        
        return QueryResponse(**result)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing query: {str(e)}"
        )


@router.get(
    "/status",
    response_model=AgentStatusResponse,
    status_code=status.HTTP_200_OK,
    summary="Get Agent Status",
    description="Retrieve the current status of the AWS Support Agent including initialization state and query count."
)
async def get_agent_status(user: dict = Depends(validate_api_key)):
    """
    Get the current status of the AWS Support Agent.
    
    Returns information about:
    - Whether the agent is initialized
    - LLM type being used
    - Model name
    - Total number of queries processed
    
    Requires authentication via Bearer token.
    """
    try:
        status_info = agent_service.get_status()
        return AgentStatusResponse(**status_info)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting agent status: {str(e)}"
        )


@router.post(
    "/initialize",
    status_code=status.HTTP_200_OK,
    summary="Initialize the Agent",
    description="Initialize or re-initialize the AWS Support Agent with the knowledge base."
)
async def initialize_agent(force_reinit: bool = False, user: dict = Depends(validate_api_key)):
    """
    Initialize the AWS Support Agent.
    
    - **force_reinit**: Force re-initialization even if already initialized (optional, default: False)
    
    This endpoint loads the knowledge base, creates embeddings, and initializes the LLM.
    First-time initialization may take a few seconds.
    
    Requires authentication via Bearer token.
    """
    try:
        success = agent_service.initialize_agent(force_reinit=force_reinit)
        
        if success:
            return {
                "status": "success",
                "message": "AWS Support Agent initialized successfully",
                "timestamp": datetime.now().isoformat()
            }
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to initialize agent"
            )
            
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error initializing agent: {str(e)}"
        )


@router.get(
    "/config",
    response_model=ConfigResponse,
    status_code=status.HTTP_200_OK,
    summary="Get Agent Configuration",
    description="Retrieve the current configuration of the AWS Support Agent."
)
async def get_agent_config(user: dict = Depends(validate_api_key)):
    """
    Get the current configuration of the AWS Support Agent.
    
    Returns information about:
    - LLM type (openai, ollama, groq)
    - Model name
    - Temperature setting
    - Max tokens setting
    
    Requires authentication via Bearer token.
    """
    try:
        config = agent_service.get_config()
        return ConfigResponse(**config)
    except RuntimeError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting agent configuration: {str(e)}"
        )
