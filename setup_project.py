import os

def create_project_structure():
    # Base directory
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Directories to create
    directories = [
        "agent",
        "assets",
        "assets/llm-agent",
        "assets/slackbot",
        "configs",
        "materializers",
        "pipelines",
        "pipelines/scripts",
        "steps",
        "scripts"
    ]
    
    # Create directories
    for directory in directories:
        dir_path = os.path.join(base_dir, directory)
        os.makedirs(dir_path, exist_ok=True)
        print(f"Created directory: {dir_path}")
        
        # Create empty __init__.py in each Python package directory
        if directory not in ["assets", "assets/llm-agent", "assets/slackbot", "scripts"]:
            init_file = os.path.join(dir_path, "__init__.py")
            with open(init_file, 'w') as f:
                pass
            print(f"Created file: {init_file}")
    
    # List of files to create
    files = [
        "agent/agent_executor_materializer.py",
        "agent/prompt.py",
        "configs/agent_config.yaml",
        "materializers/faiss_materializer.py",
        "pipelines/agent_creator.py",
        "pipelines/scripts/production_deploy.sh",
        "steps/agent_creator.py",
        "steps/index_generator.py",
        "steps/url_scraper.py",
        "steps/url_scraping_utils.py",
        "steps/web_url_loader.py",
        ".dockerignore",
        ".flake8",
        ".gitignore",
        "README.md",
        "__init__.py",
        "pyproject.toml",
        "requirements.txt",
        "run.ipynb",
        "run.py",
        ".gitmodules",
        ".typo.toml",
        "ADDING_PROJECTS.md",
        "CODE-OF-CONDUCT.md",
        "CONTRIBUTING.md",
        "LICENSE"
    ]
    
    
    for file_path in files:
        full_path = os.path.join(base_dir, file_path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, 'w') as f:
            pass
        print(f"Created file: {full_path}")
    

    with open(os.path.join(base_dir, "requirements.txt"), 'w') as f:
        f.write("# Project dependencies\n")
        f.write("numpy\n")
        f.write("pandas\n")
        f.write("python-dotenv\n")
        f.write("fastapi\n")
        f.write("uvicorn\n")
    
    with open(os.path.join(base_dir, "README.md"), 'w') as f:
        f.write("# AWS Support Agent\n\n")
        f.write("Project for AWS support automation and management.\n")
    
    with open(os.path.join(base_dir, ".gitignore"), 'w') as f:
        f.write("# Python\n")
        f.write("__pycache__/\n")
        f.write("*.py[cod]\n")
        f.write("*$py.class\n")
        f.write("\n# Environment variables\n")
        f.write(".env\n")
        f.write("\n# Virtual Environment\n")
        f.write("venv/\n")
        f.write("env/\n")
        f.write("ENV/\n")
        f.write("\n# IDE\n")
        f.write(".vscode/\n")
        f.write(".idea/\n")
    
    print("\nProject structure created successfully!")

if __name__ == "__main__":
    create_project_structure()
