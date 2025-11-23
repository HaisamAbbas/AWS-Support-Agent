"""
Agent service to manage AWS Support Agent lifecycle and queries.
This module implements a singleton pattern to ensure only one agent instance exists.
"""
import time
from typing import Optional, Tuple, Dict, Any
from datetime import datetime
from langchain.schema.vectorstore import VectorStore
from langchain_community.docstore.document import Document

from steps.index_generator import index_generator
from steps.agent_creator import aws_agent_creator, AgentParameters
from api.config import settings


class AgentService:
    """
    Singleton service for managing the AWS Support Agent.
    Handles initialization, query processing, and state management.
    """
    
    _instance = None
    _initialized = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AgentService, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        """Initialize the agent service."""
        if not self._initialized:
            self.agent = None
            self.tools = None
            self.executor = None
            self.vector_store = None
            self.query_count = 0
            self.config = None
            self._initialized = True
    
    def initialize_agent(self, force_reinit: bool = False) -> bool:
        """
        Initialize the AWS Support Agent with default documents.
        
        Args:
            force_reinit: Force re-initialization even if already initialized
            
        Returns:
            True if initialization successful, False otherwise
        """
        if self.executor is not None and not force_reinit:
            print("[INFO] Agent already initialized")
            return True
        
        try:
            print("[INFO] Initializing AWS Support Agent...")
            
            # Create sample AWS documents
            documents = self._create_sample_documents()
            
            # Create vector store
            print(f"[INFO] Creating vector store with {len(documents)} documents...")
            self.vector_store = index_generator(documents)
            print("[INFO] Vector store created successfully")
            
            # Create agent configuration
            self.config = AgentParameters(
                llm_type=settings.llm_type,
                groq_api_key=settings.groq_api_key,
                groq_model_name=settings.groq_model_name,
                openai_api_key=settings.openai_api_key,
                openai_model_name=settings.openai_model_name,
                ollama_model_name=settings.ollama_model_name,
                temperature=settings.temperature,
                max_tokens=settings.max_tokens
            )
            
            # Create agent
            print(f"[INFO] Creating AWS Support Agent with {self.config.llm_type} LLM...")
            self.agent, self.tools, self.executor = aws_agent_creator(
                vector_store=self.vector_store,
                config=self.config
            )
            
            print("[SUCCESS] AWS Support Agent initialized successfully!")
            return True
            
        except Exception as e:
            print(f"[ERROR] Failed to initialize agent: {e}")
            self.agent = None
            self.tools = None
            self.executor = None
            self.vector_store = None
            raise
    
    def _create_sample_documents(self) -> list:
        """Create sample AWS documentation documents."""
        return [
            Document(
                page_content="Amazon Web Services (AWS) is a comprehensive cloud platform offering over 200 fully-featured services from data centers globally. AWS services include EC2 for compute, S3 for storage, Lambda for serverless computing, RDS for databases, CloudFront for CDN, Route 53 for DNS, VPC for networking, and many more. AWS helps organizations move faster, lower IT costs, and scale applications.",
                metadata={"source": "aws_overview", "category": "general"}
            ),
            Document(
                page_content="AWS EC2 (Elastic Compute Cloud) provides scalable computing capacity in the AWS cloud. You can use EC2 to launch virtual servers, known as instances, and manage them according to your application needs. EC2 offers various instance types optimized for different use cases including general purpose, compute optimized, memory optimized, storage optimized, and accelerated computing instances. You can scale up or down quickly based on demand.",
                metadata={"source": "ec2_documentation", "category": "compute"}
            ),
            Document(
                page_content="AWS S3 (Simple Storage Service) is object storage built to store and retrieve any amount of data from anywhere on the web. S3 offers industry-leading scalability, data availability, security, and performance. It's designed for 99.999999999% (11 9's) of durability. You can use S3 for backup and restore, archive, data lakes, websites, mobile applications, IoT devices, and big data analytics. S3 supports different storage classes for different access patterns and cost optimization.",
                metadata={"source": "s3_documentation", "category": "storage"}
            ),
            Document(
                page_content="AWS Lambda is a serverless compute service that runs your code in response to events and automatically manages the underlying compute resources for you. You can use Lambda to extend other AWS services with custom logic, or create your own back-end services. Lambda executes your code only when needed and scales automatically, from a few requests per day to thousands per second. You pay only for the compute time you consume - there is no charge when your code is not running.",
                metadata={"source": "lambda_documentation", "category": "compute"}
            ),
            Document(
                page_content="AWS IAM (Identity and Access Management) enables you to manage access to AWS services and resources securely. Using IAM, you can create and manage AWS users and groups, and use permissions to allow and deny their access to AWS resources. IAM is a feature of your AWS account offered at no additional charge. You can use IAM to control who is authenticated (signed in) and authorized (has permissions) to use resources. Best practices include: using multi-factor authentication, rotating credentials regularly, applying least-privilege principle, and using roles for applications.",
                metadata={"source": "iam_documentation", "category": "security"}
            ),
            Document(
                page_content="AWS CloudFormation provides a common language for describing and provisioning AWS infrastructure. You can use CloudFormation to describe your entire AWS infrastructure and have it created and managed in an automated and secure way. CloudFormation uses templates written in JSON or YAML format. It supports infrastructure as code, allowing you to version control your infrastructure. CloudFormation automatically handles dependencies between resources and provides rollback capabilities in case of errors.",
                metadata={"source": "cloudformation_documentation", "category": "infrastructure"}
            ),
            Document(
                page_content="AWS RDS (Relational Database Service) makes it easy to set up, operate, and scale a relational database in the cloud. RDS supports multiple database engines including Amazon Aurora, PostgreSQL, MySQL, MariaDB, Oracle, and Microsoft SQL Server. It provides cost-efficient and resizable capacity while automating time-consuming administration tasks such as hardware provisioning, database setup, patching and backups. RDS offers automated backups, database snapshots, automatic host replacement, and read replicas for improved performance.",
                metadata={"source": "rds_documentation", "category": "database"}
            ),
            Document(
                page_content="AWS VPC (Virtual Private Cloud) lets you provision a logically isolated section of the AWS Cloud where you can launch AWS resources in a virtual network that you define. You have complete control over your virtual networking environment, including selection of your own IP address range, creation of subnets, and configuration of route tables and network gateways. You can use both IPv4 and IPv6 for most resources in your VPC. VPC provides advanced security features including security groups and network access control lists.",
                metadata={"source": "vpc_documentation", "category": "networking"}
            ),
            Document(
                page_content="AWS CloudWatch is a monitoring and observability service. It provides data and actionable insights to monitor your applications, respond to system-wide performance changes, optimize resource utilization, and get a unified view of operational health. CloudWatch collects monitoring and operational data in the form of logs, metrics, and events. You can use CloudWatch to detect anomalous behavior, set alarms, visualize logs and metrics, take automated actions, troubleshoot issues, and discover insights.",
                metadata={"source": "cloudwatch_documentation", "category": "monitoring"}
            ),
            Document(
                page_content="AWS ECS (Elastic Container Service) and EKS (Elastic Kubernetes Service) are container orchestration services. ECS is a fully managed container orchestration service that makes it easy to deploy, manage, and scale containerized applications. EKS is a managed Kubernetes service that makes it easy to run Kubernetes on AWS without needing to install and operate your own Kubernetes control plane. Both services integrate deeply with AWS services for networking, security, monitoring, and scaling.",
                metadata={"source": "container_documentation", "category": "containers"}
            )
        ]
    
    def query_agent(self, query: str, include_sources: bool = False) -> Dict[str, Any]:
        """
        Query the AWS Support Agent.
        
        Args:
            query: User's question about AWS
            include_sources: Whether to include source documents
            
        Returns:
            Dictionary containing response and metadata
        """
        if self.executor is None:
            raise RuntimeError("Agent not initialized. Please initialize the agent first.")
        
        start_time = time.time()
        
        try:
            # Execute query
            response = self.executor.invoke({"input": query})
            
            # Extract response text
            response_text = response.get("output", str(response)) if isinstance(response, dict) else str(response)
            
            # Extract sources if requested
            sources = None
            if include_sources and isinstance(response, dict):
                # Try to extract source documents from intermediate steps
                if "intermediate_steps" in response:
                    sources = []
                    for step in response.get("intermediate_steps", []):
                        if len(step) > 1 and hasattr(step[1], 'metadata'):
                            source = step[1].metadata.get('source', 'unknown')
                            if source not in sources:
                                sources.append(source)
            
            processing_time = time.time() - start_time
            self.query_count += 1
            
            return {
                "query": query,
                "response": response_text,
                "sources": sources,
                "processing_time": round(processing_time, 2),
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            processing_time = time.time() - start_time
            raise RuntimeError(f"Error processing query: {str(e)}")
    
    def get_status(self) -> Dict[str, Any]:
        """
        Get the current status of the agent.
        
        Returns:
            Dictionary containing agent status information
        """
        model_name = ""
        if self.config:
            if self.config.llm_type == "groq":
                model_name = self.config.groq_model_name
            elif self.config.llm_type == "openai":
                model_name = self.config.openai_model_name
            else:
                model_name = self.config.ollama_model_name
        
        return {
            "initialized": self.executor is not None,
            "llm_type": self.config.llm_type if self.config else "not_configured",
            "model_name": model_name,
            "total_queries": self.query_count
        }
    
    def get_config(self) -> Dict[str, Any]:
        """
        Get the current agent configuration.
        
        Returns:
            Dictionary containing configuration details
        """
        if not self.config:
            raise RuntimeError("Agent not initialized")
        
        return {
            "llm_type": self.config.llm_type,
            "model_name": (
                self.config.groq_model_name if self.config.llm_type == "groq"
                else self.config.openai_model_name if self.config.llm_type == "openai"
                else self.config.ollama_model_name
            ),
            "temperature": self.config.temperature,
            "max_tokens": self.config.max_tokens
        }


agent_service = AgentService()
