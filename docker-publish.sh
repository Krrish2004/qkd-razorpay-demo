#!/bin/bash

# Docker Hub Publishing Script for QKD-Razorpay Demo
# This script helps you publish your Docker image to Docker Hub

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if Docker is running
check_docker() {
    if ! docker info >/dev/null 2>&1; then
        print_error "Docker is not running. Please start Docker first."
        exit 1
    fi
}

# Function to get Docker Hub username
get_username() {
    if [ -z "$DOCKER_USERNAME" ]; then
        echo -n "Enter your Docker Hub username: "
        read DOCKER_USERNAME
    fi
    
    if [ -z "$DOCKER_USERNAME" ]; then
        print_error "Username is required"
        exit 1
    fi
}

# Function to login to Docker Hub
docker_login() {
    print_status "Logging into Docker Hub..."
    
    # Try different login methods
    if ! docker login -u "$DOCKER_USERNAME" 2>/dev/null; then
        print_warning "Standard login failed, trying alternative method..."
        
        # Alternative: Use environment variable for password
        if [ -n "$DOCKER_PASSWORD" ]; then
            echo "$DOCKER_PASSWORD" | docker login -u "$DOCKER_USERNAME" --password-stdin
        else
            print_status "Please enter your Docker Hub password when prompted:"
            docker login -u "$DOCKER_USERNAME"
        fi
    fi
    
    print_success "Successfully logged into Docker Hub"
}

# Function to tag and push image
tag_and_push() {
    local image_name="$1"
    local tag="$2"
    local dockerhub_repo="$DOCKER_USERNAME/qkd-razorpay-demo"
    
    print_status "Tagging image: $image_name -> $dockerhub_repo:$tag"
    docker tag "$image_name" "$dockerhub_repo:$tag" || {
        print_error "Failed to tag image"
        exit 1
    }
    
    print_status "Pushing image to Docker Hub: $dockerhub_repo:$tag"
    docker push "$dockerhub_repo:$tag" || {
        print_error "Failed to push image"
        exit 1
    }
    
    print_success "Successfully pushed: $dockerhub_repo:$tag"
}

# Function to publish images
publish() {
    check_docker
    get_username
    docker_login
    
    print_status "Available QKD images:"
    docker images | grep qkd
    echo
    
    # Tag and push the main image
    local main_image="qkd-razorpay-demo:latest"
    
    if docker images | grep -q "qkd-razorpay-demo.*latest"; then
        print_status "Publishing main image..."
        tag_and_push "$main_image" "latest"
        
        # Also tag with version
        local version=$(date +"%Y.%m.%d")
        tag_and_push "$main_image" "$version"
        
        print_success "Image published successfully!"
        echo
        print_status "Your image is now available at:"
        echo "  docker pull $DOCKER_USERNAME/qkd-razorpay-demo:latest"
        echo "  docker pull $DOCKER_USERNAME/qkd-razorpay-demo:$version"
        echo
        print_status "Docker Hub URL:"
        echo "  https://hub.docker.com/r/$DOCKER_USERNAME/qkd-razorpay-demo"
        
    else
        print_error "Main image 'qkd-razorpay-demo:latest' not found"
        print_status "Available images:"
        docker images | grep qkd
        exit 1
    fi
}

# Function to create repository README
create_readme() {
    local username="$1"
    cat > DOCKER_HUB_README.md << EOF
# QKD-Razorpay Demo - Docker Image

A comprehensive quantum cryptography demonstration combining Quantum Key Distribution (QKD) with Razorpay payment integration.

## 🚀 Quick Start

\`\`\`bash
# Pull and run the image
docker run -d -p 5000:5000 -v \$(pwd)/static:/app/static $username/qkd-razorpay-demo:latest

# Access the application
open http://localhost:5000
\`\`\`

## 🎯 Features

- **Quantum Key Distribution**: BB84 protocol simulation using Qiskit
- **Payment Integration**: Razorpay API for secure transactions  
- **AI Fraud Detection**: Machine learning-based fraud analysis
- **Modern UI**: Tailwind CSS with dark mode support
- **Interactive Presentation**: Educational quantum cryptography slides

## 📋 What's Included

- Python 3.12 runtime environment
- Qiskit for quantum computing simulations
- Flask web framework with modern frontend
- Pre-trained ML models for fraud detection
- Complete quantum cryptography educational content

## 🔧 Usage

### Basic Run
\`\`\`bash
docker run -p 5000:5000 $username/qkd-razorpay-demo
\`\`\`

### With Persistent Storage
\`\`\`bash
docker run -d \\
  -p 5000:5000 \\
  -v \$(pwd)/static:/app/static \\
  -v \$(pwd)/models:/app/models \\
  $username/qkd-razorpay-demo
\`\`\`

### Using Docker Compose
\`\`\`yaml
version: '3.8'
services:
  qkd-app:
    image: $username/qkd-razorpay-demo:latest
    ports:
      - "5000:5000"
    volumes:
      - ./static:/app/static
      - ./models:/app/models
\`\`\`

## 🌐 Access Points

- **Main Application**: http://localhost:5000
- **QKD Presentation**: http://localhost:5000/presentation  
- **API Endpoints**: http://localhost:5000/api/simulations

## 📊 Image Details

- **Base Image**: python:3.12-slim
- **Size**: ~10GB (includes quantum computing libraries)
- **Architecture**: linux/amd64
- **Exposed Port**: 5000

## 🔒 Security Features

- Non-root user execution
- Minimal attack surface with slim base image
- Secure quantum key generation
- Input validation and sanitization

## 📖 Documentation

For complete documentation, source code, and development setup:
- **GitHub Repository**: [Add your GitHub URL here]
- **Docker Guide**: See DOCKER_README.md in the repository

## 🏷️ Tags

- \`latest\` - Most recent stable version
- \`YYYY.MM.DD\` - Date-based version tags

## 🤝 Contributing

This is an educational demonstration project showcasing quantum cryptography concepts with practical payment integration.

## 📄 License

[Add your license information here]
EOF

    print_success "Created DOCKER_HUB_README.md - you can copy this content to your Docker Hub repository description"
}

# Function to show help
help() {
    echo "QKD-Razorpay Docker Publishing Script"
    echo
    echo "Usage: $0 [COMMAND]"
    echo
    echo "Commands:"
    echo "  publish       Tag and push images to Docker Hub"
    echo "  readme        Generate README content for Docker Hub"
    echo "  login         Login to Docker Hub"
    echo "  help          Show this help message"
    echo
    echo "Environment Variables:"
    echo "  DOCKER_USERNAME    Your Docker Hub username"
    echo "  DOCKER_PASSWORD    Your Docker Hub password (optional)"
    echo
    echo "Examples:"
    echo "  $0 publish                    # Interactive publish"
    echo "  DOCKER_USERNAME=myuser $0 publish  # With username preset"
    echo "  $0 readme                     # Generate Docker Hub README"
}

# Main script logic
case "${1:-help}" in
    publish)
        publish
        ;;
    readme)
        get_username
        create_readme "$DOCKER_USERNAME"
        ;;
    login)
        get_username
        docker_login
        ;;
    help|*)
        help
        ;;
esac 