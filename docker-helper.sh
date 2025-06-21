#!/bin/bash

# QKD-Razorpay Docker Helper Script
# This script provides convenient commands for Docker operations

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

# Function to build the Docker image
build() {
    print_status "Building QKD-Razorpay Docker image..."
    check_docker
    
    docker build -t qkd-razorpay-demo . || {
        print_error "Failed to build Docker image"
        exit 1
    }
    
    print_success "Docker image built successfully!"
}

# Function to run the container
run() {
    print_status "Starting QKD-Razorpay container..."
    check_docker
    
    # Stop existing container if running
    docker stop qkd-razorpay-container 2>/dev/null || true
    docker rm qkd-razorpay-container 2>/dev/null || true
    
    # Run new container
    docker run -d \
        --name qkd-razorpay-container \
        -p 5000:5000 \
        -v "$(pwd)/static:/app/static" \
        -v "$(pwd)/models:/app/models" \
        qkd-razorpay-demo || {
        print_error "Failed to start container"
        exit 1
    }
    
    print_success "Container started successfully!"
    print_status "Application will be available at: http://localhost:5000"
    print_status "Presentation available at: http://localhost:5000/presentation"
}

# Function to use docker-compose
compose_up() {
    print_status "Starting services with docker-compose..."
    check_docker
    
    docker compose up --build -d || {
        print_error "Failed to start services with docker-compose"
        exit 1
    }
    
    print_success "Services started successfully!"
    print_status "Application available at: http://localhost:5000"
}

# Function to use docker-compose with production profile
compose_prod() {
    print_status "Starting services in production mode..."
    check_docker
    
    docker compose --profile production up --build -d || {
        print_error "Failed to start services in production mode"
        exit 1
    }
    
    print_success "Production services started successfully!"
    print_status "Application available at: http://localhost:80"
    print_status "Direct app access: http://localhost:5000"
}

# Function to stop services
stop() {
    print_status "Stopping QKD-Razorpay services..."
    
    # Stop docker-compose services
    docker compose down 2>/dev/null || true
    
    # Stop standalone container
    docker stop qkd-razorpay-container 2>/dev/null || true
    docker rm qkd-razorpay-container 2>/dev/null || true
    
    print_success "Services stopped successfully!"
}

# Function to show logs
logs() {
    print_status "Showing application logs..."
    
    if docker compose ps -q qkd-razorpay-app >/dev/null 2>&1; then
        docker compose logs -f qkd-razorpay-app
    elif docker ps -q -f name=qkd-razorpay-container >/dev/null 2>&1; then
        docker logs -f qkd-razorpay-container
    else
        print_warning "No running QKD-Razorpay containers found"
    fi
}

# Function to show status
status() {
    print_status "QKD-Razorpay Docker Status:"
    echo
    
    # Check docker-compose services
    if docker compose ps -q >/dev/null 2>&1; then
        echo "Docker Compose Services:"
        docker compose ps
        echo
    fi
    
    # Check standalone container
    if docker ps -q -f name=qkd-razorpay-container >/dev/null 2>&1; then
        echo "Standalone Container:"
        docker ps -f name=qkd-razorpay-container
        echo
    fi
    
    # Check if application is responding
    if curl -s http://localhost:5000 >/dev/null 2>&1; then
        print_success "Application is responding at http://localhost:5000"
    else
        print_warning "Application is not responding at http://localhost:5000"
    fi
}

# Function to clean up Docker resources
cleanup() {
    print_status "Cleaning up Docker resources..."
    
    # Stop services
    stop
    
    # Remove images
    docker rmi qkd-razorpay-demo 2>/dev/null || true
    
    # Clean up unused resources
    docker system prune -f
    
    print_success "Cleanup completed!"
}

# Function to show help
help() {
    echo "QKD-Razorpay Docker Helper Script"
    echo
    echo "Usage: $0 [COMMAND]"
    echo
    echo "Commands:"
    echo "  build         Build the Docker image"
    echo "  run           Run the application in a standalone container"
    echo "  compose       Start services using docker-compose"
    echo "  prod          Start services in production mode (with nginx)"
    echo "  stop          Stop all services"
    echo "  logs          Show application logs"
    echo "  status        Show status of running services"
    echo "  cleanup       Clean up Docker resources"
    echo "  help          Show this help message"
    echo
    echo "Examples:"
    echo "  $0 build         # Build the Docker image"
    echo "  $0 compose       # Start with docker-compose"
    echo "  $0 prod          # Start in production mode"
    echo "  $0 logs          # View logs"
    echo "  $0 stop          # Stop all services"
}

# Main script logic
case "${1:-help}" in
    build)
        build
        ;;
    run)
        build
        run
        ;;
    compose)
        compose_up
        ;;
    prod)
        compose_prod
        ;;
    stop)
        stop
        ;;
    logs)
        logs
        ;;
    status)
        status
        ;;
    cleanup)
        cleanup
        ;;
    help|*)
        help
        ;;
esac