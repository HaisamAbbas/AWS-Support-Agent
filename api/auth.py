"""
Authentication middleware and utilities for API key validation.
"""
from fastapi import HTTPException, Security, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional

# Security scheme
security = HTTPBearer()

# In production, store API keys in a database or secrets manager
# For demo purposes, we'll accept any non-empty key
VALID_API_KEYS = {
    "demo-key-123": {"username": "demo_user", "role": "user"},
    "admin-key-456": {"username": "admin", "role": "admin"},
}

def validate_api_key(credentials: HTTPAuthorizationCredentials = Security(security)) -> dict:
    """
    Validate API key from Authorization header.
    
    Args:
        credentials: HTTP Bearer token credentials
        
    Returns:
        User information dict
        
    Raises:
        HTTPException: If API key is invalid
    """
    api_key = credentials.credentials
    
    # For demo: accept any non-empty key
    # In production: validate against database or secrets manager
    if not api_key or len(api_key) < 5:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Check if key exists in our valid keys (demo only)
    user_info = VALID_API_KEYS.get(api_key)
    
    if user_info:
        return user_info
    
    # For demo: accept any key and return generic user
    return {"username": "user", "role": "user", "api_key": api_key}


def validate_api_key_optional(
    credentials: Optional[HTTPAuthorizationCredentials] = Security(security)
) -> Optional[dict]:
    """
    Optional API key validation.
    Returns None if no credentials provided.
    """
    if not credentials:
        return None
    return validate_api_key(credentials)
