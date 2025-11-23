"""
FastAPI Main Application
AWS Support Agent API Backend
"""
from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from datetime import datetime
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api.config import settings
from api.models import HealthResponse
from api.routers import agent, auth_router
from api.routers.websocket import socket_app

# Create FastAPI application
app = FastAPI(
    title=settings.app_name,
    description=settings.app_description,
    version=settings.app_version,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=settings.cors_credentials,
    allow_methods=settings.cors_methods,
    allow_headers=settings.cors_headers,
)

# Include routers
app.include_router(agent.router)
app.include_router(auth_router.router)

# Mount Socket.IO app for WebSocket streaming
app.mount("/ws", socket_app)


@app.on_event("startup")
async def startup_event():
    """
    Run on application startup.
    """
    print("=" * 60)
    print(f"{settings.app_name} v{settings.app_version}")
    print("=" * 60)
    print(f"📚 Documentation: http://localhost:8000/docs")
    print(f"🔄 ReDoc: http://localhost:8000/redoc")
    print(f"🤖 LLM Type: {settings.llm_type}")
    print(f"📝 Model: {settings.groq_model_name if settings.llm_type == 'groq' else settings.openai_model_name if settings.llm_type == 'openai' else settings.ollama_model_name}")
    print(f"🔐 Authentication: Enabled (API Key)")
    print(f"⚡ WebSocket Streaming: Enabled at /ws")
    print("=" * 60)
    print("⚠️  Note: Call /agent/initialize before making queries")
    print("=" * 60)


@app.on_event("shutdown")
async def shutdown_event():
    """
    Run on application shutdown.
    """
    print("\n" + "=" * 60)
    print("Shutting down AWS Support Agent API...")
    print("=" * 60)


@app.get(
    "/",
    response_model=HealthResponse,
    status_code=status.HTTP_200_OK,
    summary="Root Endpoint",
    description="Returns basic API information and health status."
)
async def root():
    """
    Root endpoint - returns API health status and basic information.
    """
    return HealthResponse(
        status="healthy",
        version=settings.app_version,
        timestamp=datetime.now().isoformat()
    )


@app.get(
    "/health",
    response_model=HealthResponse,
    status_code=status.HTTP_200_OK,
    summary="Health Check",
    description="Health check endpoint for monitoring and load balancers."
)
async def health_check():
    """
    Health check endpoint.
    """
    return HealthResponse(
        status="healthy",
        version=settings.app_version,
        timestamp=datetime.now().isoformat()
    )


@app.exception_handler(404)
async def not_found_handler(request, exc):
    """
    Custom 404 handler.
    """
    return JSONResponse(
        status_code=404,
        content={
            "error": "Not Found",
            "message": f"The requested endpoint {request.url.path} was not found",
            "timestamp": datetime.now().isoformat()
        }
    )


@app.exception_handler(500)
async def internal_error_handler(request, exc):
    """
    Custom 500 handler.
    """
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "message": "An unexpected error occurred",
            "detail": str(exc) if settings.debug else None,
            "timestamp": datetime.now().isoformat()
        }
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug
    )
