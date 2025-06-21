#!/bin/bash

# Startup script for QKD-Razorpay Docker container

# Set default environment variables
export FLASK_APP=${FLASK_APP:-app.py}
export FLASK_ENV=${FLASK_ENV:-production}
export PORT=${PORT:-5000}

# Create necessary directories
mkdir -p static
mkdir -p models
mkdir -p templates

# Set permissions
chmod -R 755 static

# Start the Flask application
echo "Starting QKD-Razorpay Demo on port $PORT..."
python app.py 