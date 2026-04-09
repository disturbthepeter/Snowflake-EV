import os
from pathlib import Path

# Define the directory structure
folders = [
    "infra",
    "src/ingestion",
    "src/transformations",
    "src/shared",
    "models/dynamic_tables",
    "models/semantic",
    "apps/streamlit",
    "notebooks",
    "tests"
]

files = {
    "README.md": "# EV Population Analytics\nArchitectural overview and setup instructions.",
    ".gitignore": "*.pyc\n.env\n__pycache__/\n.DS_Store",
    "requirements.txt": "snowflake-snowpark-python\nstreamlit\nplotly",
    "infra/databases.sql": "-- DDL for Database/Schema setup",
    "infra/warehouses.sql": "-- DDL for Virtual Warehouses",
    "infra/rbac.sql": "-- Role and Permission definitions"
}

def build_structure():
    # Create directories
    for folder in folders:
        Path(folder).mkdir(parents=True, exist_ok=True)
        print(f"Created folder: {folder}")

    # Create boilerplate files
    for file_path, content in files.items():
        with open(file_path, "w") as f:
            f.write(content)
        print(f"Created file: {file_path}")

if __name__ == "__main__":
    build_structure()
    print("\n✅ Skeleton directory structure complete.")
