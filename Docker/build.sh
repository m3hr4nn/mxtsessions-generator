#!/bin/bash

# MXTSessions Generator - Docker Build Script
# Usage: ./build.sh [dev|prod]

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
IMAGE_NAME="mxtsessions-generator"
VERSION="1.0.0"

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

# Function to build development image
build_dev() {
    print_status "Building development image..."
    docker build -t ${IMAGE_NAME}:dev -t ${IMAGE_NAME}:latest .
    print_success "Development image built successfully!"
}

# Function to build production image
build_prod() {
    print_status "Building production image..."
    docker build -f Dockerfile.prod -t ${IMAGE_NAME}:prod -t ${IMAGE_NAME}:${VERSION} .
    print_success "Production image built successfully!"
}

# Function to show usage
show_usage() {
    echo "Usage: $0 [dev|prod|both]"
    echo ""
    echo "Options:"
    echo "  dev     Build development image with Flask dev server"
    echo "  prod    Build production image with Gunicorn"
    echo "  both    Build both development and production images"
    echo ""
    echo "If no option is provided, development image will be built."
}

# Main script
main() {
    echo "🚀 MXTSessions Generator Docker Build Script"
    echo "=============================================="
    
    # Check if Docker is running
    if ! docker info > /dev/null 2>&1; then
        print_error "Docker is not running. Please start Docker and try again."
        exit 1
    fi
    
    # Parse arguments
    case "${1:-dev}" in
        "dev")
            build_dev
            ;;
        "prod")
            build_prod
            ;;
        "both")
            build_dev
            build_prod
            ;;
        "help"|"-h"|"--help")
            show_usage
            exit 0
            ;;
        *)
            print_error "Invalid option: $1"
            show_usage
            exit 1
            ;;
    esac
    
    # Show built images
    print_status "Built images:"
    docker images ${IMAGE_NAME}
    
    echo ""
    print_success "Build completed! 🎉"
    echo ""
    echo "To run the application:"
    echo "  Development: docker run -p 5000:5000 ${IMAGE_NAME}:dev"
    echo "  Production:  docker run -p 5000:5000 ${IMAGE_NAME}:prod"
    echo "  With compose: docker-compose up"
}

# Run main function
main "$@"
