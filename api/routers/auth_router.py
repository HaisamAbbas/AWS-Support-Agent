"""
Authentication Router
Handles login and API key validation.
"""
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from datetime import datetime

router = APIRouter(
    prefix="/auth",
    tags=["authentication"]
)


class LoginRequest(BaseModel):
    """Login request model."""
    api_key: str


class LoginResponse(BaseModel):
    """Login response model."""
    success: bool
    message: str
    username: str
    timestamp: str


@router.post(
    "/login",
    response_model=LoginResponse,
    status_code=status.HTTP_200_OK,
    summary="Login with API Key",
    description="Validate API key and return user information."
)
async def login(request: LoginRequest):
    """
    Login endpoint - validates API key.
    
    For demo purposes, any key with length >= 5 is accepted.
    In production, validate against a database or secrets manager.
    """
    api_key = request.api_key.strip()
    
    if not api_key or len(api_key) < 5:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key. Must be at least 5 characters."
        )
    
    # Demo: accept any valid-length key
    # In production: check database or secrets manager
    known_keys = {
        "demo-key-123": "demo_user",
        "admin-key-456": "admin_user"
    }
    
    username = known_keys.get(api_key, "user")
    
    return LoginResponse(
        success=True,
        message="Login successful",
        username=username,
        timestamp=datetime.now().isoformat()
    )


@router.get(
    "/validate",
    summary="Validate Current Session",
    description="Check if the current API key is valid."
)
async def validate_session():
    """
    Validate the current session.
    This endpoint requires authentication.
    """
    return {
        "valid": True,
        "message": "Session is valid",
        "timestamp": datetime.now().isoformat()
    }
