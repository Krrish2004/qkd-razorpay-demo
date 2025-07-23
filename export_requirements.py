#!/usr/bin/env python3
"""
Export script to generate requirements.txt files from Poetry dependencies
for backward compatibility with pip-based installations.
"""

import sys
from pathlib import Path

try:
    import tomllib  # Python 3.11+
except ImportError:
    try:
        import tomli as tomllib  # Fallback for older Python
    except ImportError:
        print("❌ Neither tomllib nor tomli available. Install with: pip install tomli")
        sys.exit(1)

def load_pyproject():
    """Load pyproject.toml file"""
    pyproject_path = Path("pyproject.toml")
    if not pyproject_path.exists():
        print("❌ pyproject.toml not found!")
        return None
    
    with open(pyproject_path, "rb") as f:
        return tomllib.load(f)

def format_dependency(name, constraint):
    """Format a dependency specification"""
    if isinstance(constraint, str):
        return f"{name}{constraint}"
    elif isinstance(constraint, dict):
        version = constraint.get("version", "")
        return f"{name}{version}"
    return name

def export_requirements() -> bool:
    """Export requirements to requirements-poetry.txt files"""
    print("📦 Exporting Poetry dependencies to requirements files...")
    
    pyproject = load_pyproject()
    if not pyproject:
        return False
    
    # Get dependencies
    tool_poetry = pyproject.get("tool", {}).get("poetry", {})
    dependencies = tool_poetry.get("dependencies", {})
    dev_dependencies = tool_poetry.get("group", {}).get("dev", {}).get("dependencies", {})
    
    # Remove python from dependencies
    dependencies.pop("python", None)
    
    # Generate production requirements
    prod_requirements = []
    for name, constraint in dependencies.items():
        req = format_dependency(name, constraint)
        prod_requirements.append(req)
    
    # Generate development requirements  
    dev_requirements = []
    for name, constraint in dev_dependencies.items():
        req = format_dependency(name, constraint)
        dev_requirements.append(req)
    
    # Write production requirements
    with open("requirements-poetry.txt", "w") as f:
        f.write("# Generated from pyproject.toml by export_requirements.py\n")
        f.write("# For Poetry users: use 'poetry install' instead\n")
        f.write("# For pip users: pip install -r requirements-poetry.txt\n\n")
        for req in sorted(prod_requirements):
            f.write(f"{req}\n")
    
    # Write development requirements
    with open("requirements-poetry-dev.txt", "w") as f:
        f.write("# Generated from pyproject.toml by export_requirements.py\n")
        f.write("# Install production dependencies first: pip install -r requirements-poetry.txt\n")
        f.write("# Then install dev dependencies: pip install -r requirements-poetry-dev.txt\n\n")
        for req in sorted(dev_requirements):
            f.write(f"{req}\n")
    
    # Write combined requirements
    with open("requirements-poetry-all.txt", "w") as f:
        f.write("# Generated from pyproject.toml by export_requirements.py\n")
        f.write("# All dependencies (production + development)\n")
        f.write("# For pip users: pip install -r requirements-poetry-all.txt\n\n")
        f.write("# Production dependencies\n")
        for req in sorted(prod_requirements):
            f.write(f"{req}\n")
        f.write("\n# Development dependencies\n")
        for req in sorted(dev_requirements):
            f.write(f"{req}\n")
    
    print(f"✅ Generated requirements-poetry.txt ({len(prod_requirements)} packages)")
    print(f"✅ Generated requirements-poetry-dev.txt ({len(dev_requirements)} packages)")
    print(f"✅ Generated requirements-poetry-all.txt ({len(prod_requirements + dev_requirements)} packages)")
    
    return True

if __name__ == "__main__":
    success = export_requirements()
    sys.exit(0 if success else 1) 