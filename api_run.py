"""
FastAPI Server Entry Point
Run this file to start the AWS Support Agent API server.

Usage:
    python api_run.py
    
Or with custom settings:
    python api_run.py --host 0.0.0.0 --port 8000 --reload
"""
import os
import sys
import uvicorn
import click

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Set GROQ API key
if not os.getenv("GROQ_API_KEY"):
    raise ValueError("GROQ_API_KEY environment variable is required. Please set it in your .env file")


@click.command(
    help="""
AWS Support Agent API Server

Start the FastAPI server for the AWS Support Agent.

Examples:

  \b
  # Start the server on default port 8000
  python api_run.py

  \b
  # Start with custom host and port
  python api_run.py --host 0.0.0.0 --port 8080

  \b
  # Start with auto-reload for development
  python api_run.py --reload

  \b
  # Access the API documentation at:
  http://localhost:8000/docs
"""
)
@click.option(
    "--host",
    default="0.0.0.0",
    help="Host to bind the server to (default: 0.0.0.0)",
)
@click.option(
    "--port",
    default=8000,
    type=int,
    help="Port to bind the server to (default: 8000)",
)
@click.option(
    "--reload",
    is_flag=True,
    default=False,
    help="Enable auto-reload for development",
)
@click.option(
    "--workers",
    default=1,
    type=int,
    help="Number of worker processes (default: 1)",
)
def main(host: str, port: int, reload: bool, workers: int):
    """
    Start the FastAPI server.
    
    Args:
        host: Host to bind the server to
        port: Port to bind the server to
        reload: Enable auto-reload for development
        workers: Number of worker processes
    """
    print("=" * 70)
    print("🚀 Starting AWS Support Agent API Server")
    print("=" * 70)
    print(f"📍 Host: {host}")
    print(f"🔌 Port: {port}")
    print(f"🔄 Reload: {'Enabled' if reload else 'Disabled'}")
    print(f"👷 Workers: {workers}")
    print("=" * 70)
    print(f"📚 API Documentation: http://{host if host != '0.0.0.0' else 'localhost'}:{port}/docs")
    print(f"📖 ReDoc: http://{host if host != '0.0.0.0' else 'localhost'}:{port}/redoc")
    print("=" * 70)
    print("\n⚠️  IMPORTANT: Before making queries, initialize the agent:")
    print(f"   POST http://{host if host != '0.0.0.0' else 'localhost'}:{port}/agent/initialize")
    print("\n💡 TIP: Use Ctrl+C to stop the server")
    print("=" * 70 + "\n")
    
    try:
        uvicorn.run(
            "api.main:app",
            host=host,
            port=port,
            reload=reload,
            workers=workers if not reload else 1,  # reload doesn't work with multiple workers
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n\n" + "=" * 70)
        print("🛑 Server stopped by user")
        print("=" * 70)
    except Exception as e:
        print(f"\n\n❌ Error starting server: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
