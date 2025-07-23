# 🚀 Poetry Setup Guide for QKD-Razorpay Demo

This guide will help you set up and run the QKD-Razorpay Demo project using Poetry, ensuring it can be run directly on any system with consistent dependencies.

## 📋 Prerequisites

### System Requirements
- **Python**: 3.8.1 or higher (recommended: 3.11+)
- **Operating System**: Linux, macOS, or Windows
- **Memory**: At least 4GB RAM (8GB+ recommended for quantum simulations)
- **Storage**: 2GB free space for dependencies

### Install Poetry

Choose one of the following methods:

#### Method 1: Official Installer (Recommended)
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

#### Method 2: pip (if you prefer)
```bash
pip install poetry
```

#### Method 3: Package Manager
```bash
# On Ubuntu/Debian
sudo apt install python3-poetry

# On macOS with Homebrew
brew install poetry

# On Windows with Chocolatey
choco install poetry
```

### Add Poetry to PATH
After installation, add Poetry to your PATH:

```bash
# Add to your shell profile (.bashrc, .zshrc, etc.)
export PATH="$HOME/.local/bin:$PATH"

# Reload your shell or run:
source ~/.bashrc  # or source ~/.zshrc
```

Verify installation:
```bash
poetry --version
```

## 🛠️ Project Setup

### 1. Clone the Repository
```bash
git clone <repository-url>
cd qkd-razorpay-demo
```

### 2. Install Dependencies
```bash
# Install all dependencies (production + development)
poetry install

# OR install only production dependencies
poetry install --only=main
```

### 3. Activate the Virtual Environment
```bash
# Option 1: Use Poetry shell
poetry shell

# Option 2: Run commands with Poetry
poetry run python --version
```

## 🚀 Running the Application

### Web Application
```bash
# Using Poetry
poetry run python app.py

# Or using Make (if available)
make run-web

# Or using Poetry scripts
poetry run qkd-web
```

Access the web application at: **http://localhost:5000**

### Command Line Interface
```bash
# Basic CLI demo
poetry run python main.py

# With custom parameters
poetry run python main.py --qubits 500 --error-rate 0.01 --amount 50000

# Using Make
make run-cli

# Using Poetry scripts
poetry run qkd-cli
```

### Presentation Mode
```bash
# Start web app and navigate to /presentation
poetry run python app.py
# Then visit: http://localhost:5000/presentation
```

## 🧪 Testing the Setup

### Run Tests
```bash
# All tests
poetry run pytest

# With coverage
poetry run pytest --cov=. --cov-report=html

# Quick test
make quick-test
```

### Verify Installation
```bash
# Test core dependencies
poetry run python -c "
import qiskit
import flask
import torch
import pandas
import razorpay
print('✅ All core dependencies imported successfully!')
print('✅ Project is ready to run!')
"
```

### Run a Quick Demo
```bash
# Test quantum simulation
poetry run python -c "
from qkd_module import QKDSimulator
print('Testing QKD simulation...')
qkd = QKDSimulator(n_bits=100)
success, key = qkd.generate_quantum_keys(key_length=16)
print(f'QKD Test: {\"✅ SUCCESS\" if success else \"❌ FAILED\"}')
"
```

## 📦 Available Commands

### Using Make (Recommended)
```bash
# Show all available commands
make help

# Common commands
make install        # Install dependencies
make test          # Run tests
make format        # Format code
make lint          # Run linting
make run-web       # Start web app
make run-cli       # Run CLI demo
make clean         # Clean temporary files
```

### Using Poetry Directly
```bash
# Project management
poetry install                 # Install dependencies
poetry update                 # Update dependencies
poetry show                   # List installed packages
poetry env info              # Show environment info

# Running the application
poetry run python app.py     # Web application
poetry run python main.py    # CLI application
poetry run python run.py --web  # Alternative runner

# Development tools
poetry run pytest            # Run tests
poetry run black .          # Format code
poetry run flake8 .         # Lint code
poetry run mypy .           # Type checking
```

### Using Poetry Scripts
The project defines custom scripts in `pyproject.toml`:
```bash
poetry run qkd-demo         # Run demo via run.py
poetry run qkd-web          # Start web application
poetry run qkd-cli          # Run CLI version
```

## 🔧 Development Setup

### Full Development Environment
```bash
# Install with development dependencies
poetry install

# Set up pre-commit hooks
poetry run pre-commit install

# Or use Make for full setup
make dev
```

### Code Quality Tools
```bash
# Format code
poetry run black .
poetry run isort .

# Check code quality
poetry run flake8 .
poetry run mypy .
poetry run bandit -r .

# Run all checks
make check
```

## 📊 Project Structure

```
qkd-razorpay-demo/
├── pyproject.toml          # Poetry configuration & dependencies
├── poetry.lock            # Lock file with exact versions
├── Makefile               # Convenient development commands
├── .pre-commit-config.yaml # Code quality automation
├── 
├── app.py                 # Flask web application
├── main.py                # CLI application
├── run.py                 # Universal runner
├── 
├── qkd_module.py          # Quantum Key Distribution
├── encryption.py          # Quantum encryption
├── fraud_detection.py     # AI fraud detection
├── razorpay_api.py        # Payment integration
├── 
├── tests/                 # Test suite
├── templates/             # Web templates
├── static/                # Static assets
└── models/                # Pre-trained models
```

## 🌐 Environment Configuration

### Create `.env` File
```bash
# Copy example configuration
cp .env.example .env  # if available

# Or create manually
cat > .env << EOF
# Razorpay API Keys (Optional - uses test mode by default)
RAZORPAY_KEY_ID=rzp_test_your_key_id
RAZORPAY_KEY_SECRET=your_key_secret

# Application Settings
FLASK_ENV=development
FLASK_DEBUG=True
EOF
```

### Environment Variables
- `RAZORPAY_KEY_ID`: Your Razorpay test key ID
- `RAZORPAY_KEY_SECRET`: Your Razorpay test key secret
- `FLASK_ENV`: Flask environment (development/production)
- `PORT`: Port for web application (default: 5000)

## 🐳 Alternative: Docker Setup

If you prefer Docker over Poetry:

```bash
# Build and run with Docker
docker build -t qkd-razorpay-demo .
docker run -p 5000:5000 qkd-razorpay-demo

# Or use docker-compose
docker-compose up
```

## 🚨 Troubleshooting

### Common Issues

#### Poetry Command Not Found
```bash
# Add Poetry to PATH
export PATH="$HOME/.local/bin:$PATH"
source ~/.bashrc
```

#### Python Version Issues
```bash
# Check Python version
python3 --version

# If below 3.8.1, install newer Python
# Ubuntu/Debian:
sudo apt update
sudo apt install python3.11 python3.11-venv

# Then tell Poetry to use it:
poetry env use python3.11
```

#### Dependency Installation Fails
```bash
# Clear Poetry cache
poetry cache clear . --all

# Remove and recreate environment
poetry env remove --all
poetry install
```

#### CUDA/PyTorch Issues
```bash
# For CPU-only PyTorch (if CUDA issues)
poetry install --extras cpu

# Or modify pyproject.toml to use CPU-only torch
```

#### Permission Issues
```bash
# On Linux/macOS, ensure user has write permissions
sudo chown -R $USER:$USER ~/.local/share/pypoetry
```

### Performance Issues

#### Slow Quantum Simulations
- Reduce qubit count: `--qubits 100` instead of `--qubits 1000`
- Use fewer iterations in testing
- Ensure sufficient RAM (8GB+ recommended)

#### Memory Issues
```bash
# Monitor memory usage
poetry run python -c "
import psutil
print(f'Available memory: {psutil.virtual_memory().available / 1024**3:.1f} GB')
"
```

## 📞 Support

### Getting Help
1. **Documentation**: Check the main README.md
2. **Issues**: Create an issue in the repository
3. **Tests**: Run `make test` to verify setup

### Verify Setup
Run this comprehensive verification:

```bash
# Complete setup verification
poetry run python -c "
import sys
print(f'Python: {sys.version}')

import qiskit
print(f'Qiskit: {qiskit.__version__}')

import flask
print(f'Flask: {flask.__version__}')

import torch
print(f'PyTorch: {torch.__version__}')

from qkd_module import QKDSimulator
qkd = QKDSimulator(n_bits=50)
success, _ = qkd.generate_quantum_keys(key_length=16)
print(f'QKD Test: {'✅ PASS' if success else '❌ FAIL'}')

print('🎉 Setup verification complete!')
"
```

## 📈 Next Steps

After successful setup:

1. **Explore the Web Interface**: `make run-web`
2. **Try the CLI Demo**: `make run-cli`
3. **Run Tests**: `make test`
4. **Read the Documentation**: Check `README.md`
5. **Experiment**: Modify parameters and explore quantum cryptography!

---

**Happy quantum computing! 🚀⚛️** 