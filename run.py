"""
Main entrypoint for running the AWS Support Agent pipeline.
This file initializes and executes the pipeline that builds
an AWS-compatible agent using LangGraph, OpenAI, and FAISS.
"""

import os
import sys
import click
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from pipelines.agent_creator import aws_agent_creation_pipeline

@click.command(
    help="""
AWS Support Agent Project Runner.

Run the AWS-compatible pipeline with configurable options.

Examples:

  \b
  # Run the pipeline in local mode
  python run.py

  \b
  # Run in AWS mode (e.g., deploying artifacts to S3)
  python run.py --mode aws
"""
)
@click.option(
    "--mode",
    type=click.Choice(["local", "aws"], case_sensitive=False),
    default="local",
    help="Run mode — 'local' for development or 'aws' for deployment.",
)
def main(mode: str):
    """
    Main entry point for pipeline execution.

    Args:
        mode (str): Execution mode, either 'local' or 'aws'.
    """
    try:
        # Load GROQ API key from environment
        if not os.getenv("GROQ_API_KEY"):
            raise ValueError("GROQ_API_KEY environment variable is required")
        
        if mode.lower() == "aws":
            os.environ.setdefault("AWS_REGION", "us-east-1")
            os.environ.setdefault("S3_BUCKET_NAME", "aws-support-agent-pipeline-artifacts")

        print("[START] Launching AWS Support Agent pipeline with GROQ integration...")
        vector_store = aws_agent_creation_pipeline()

        print("[SUCCESS] Pipeline execution completed successfully with GROQ integration.")
    except Exception as e:
        print(f"[ERROR] Pipeline execution failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
