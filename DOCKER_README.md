# QKD-Razorpay Demo - Docker Deployment Guide

This guide explains how to run the QKD-Razorpay demonstration project using Docker.

## 🐳 Quick Start

### Option 1: Using Docker Compose (Recommended)

```bash
# Clone the repository
git clone <repository-url>
cd qkd-razorpay-demo

# Build and start the application
docker-compose up --build

# Access the application
# Main Application: http://localhost:5000
# Presentation: http://localhost:5000/presentation
```

### Option 2: Using Docker directly

```bash
# Build the Docker image
docker build -t qkd-razorpay-demo .

# Run the container
docker run -d \
  --name qkd-razorpay-container \
  -p 5000:5000 \
  -v $(pwd)/static:/app/static \
  -v $(pwd)/models:/app/models \
  qkd-razorpay-demo

# Access the application at http://localhost:5000
```

## 🏗️ Architecture

The Docker setup includes:

- **Main Application Container**: Python Flask app with QKD simulation
- **Nginx Reverse Proxy** (optional): For production deployments
- **Volume Mounts**: For persistent storage of generated files and models

## 📁 Docker Files

- `Dockerfile`: Main application container definition
- `docker-compose.yml`: Multi-container orchestration
- `nginx.conf`: Nginx reverse proxy configuration
- `.dockerignore`: Files to exclude from Docker build context
- `start.sh`: Container startup script

## 🔧 Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `FLASK_ENV` | `production` | Flask environment mode |
| `FLASK_APP` | `app.py` | Flask application entry point |
| `PORT` | `5000` | Port to run the application on |
| `PYTHONUNBUFFERED` | `1` | Disable Python output buffering |

### Volume Mounts

- `./static:/app/static` - Persistent storage for generated QKD visualizations
- `./models:/app/models` - ML model files for fraud detection

## 🚀 Deployment Options

### Development Mode

```bash
# Run with development settings
docker-compose up --build
```

### Production Mode (with Nginx)

```bash
# Run with nginx reverse proxy
docker-compose --profile production up --build

# Access via:
# HTTP: http://localhost:80
# HTTPS: http://localhost:443 (requires SSL setup)
```

## 🔒 Security Considerations

### For Production Deployment:

1. **SSL/TLS Configuration**:
   ```bash
   # Create SSL directory
   mkdir ssl
   # Add your SSL certificates
   cp your-cert.pem ssl/cert.pem
   cp your-key.pem ssl/key.pem
   ```

2. **Environment Variables**:
   ```bash
   # Create .env file for sensitive data
   echo "RAZORPAY_KEY_ID=your_key_id" > .env
   echo "RAZORPAY_KEY_SECRET=your_key_secret" >> .env
   ```

3. **Firewall Rules**:
   ```bash
   # Only expose necessary ports
   # Block direct access to port 5000 in production
   ```

## 📊 Monitoring and Health Checks

### Health Check Endpoint

The application includes built-in health checks:

```bash
# Check application health
curl http://localhost:5000/

# Check via Docker
docker exec qkd-razorpay-container curl -f http://localhost:5000/
```

### Logs

```bash
# View application logs
docker-compose logs -f qkd-razorpay-app

# View nginx logs (if using production profile)
docker-compose logs -f nginx
```

## 🛠️ Development

### Building Custom Images

```bash
# Build with custom tag
docker build -t qkd-razorpay:v1.0.0 .

# Build with build arguments
docker build \
  --build-arg PYTHON_VERSION=3.12 \
  -t qkd-razorpay:custom .
```

### Debugging

```bash
# Run container in interactive mode
docker run -it --rm \
  -p 5000:5000 \
  -v $(pwd)/static:/app/static \
  qkd-razorpay-demo bash

# Access running container
docker exec -it qkd-razorpay-container bash
```

## 🔄 Updates and Maintenance

### Updating the Application

```bash
# Pull latest changes
git pull origin main

# Rebuild and restart
docker-compose down
docker-compose up --build -d
```

### Backup Important Data

```bash
# Backup generated visualizations
tar -czf qkd-static-backup.tar.gz static/

# Backup simulation data (if implemented)
docker exec qkd-razorpay-container python -c "
import json
from app import simulations
with open('/tmp/simulations.json', 'w') as f:
    json.dump(simulations, f)
"
docker cp qkd-razorpay-container:/tmp/simulations.json ./simulations-backup.json
```

## 🐛 Troubleshooting

### Common Issues

1. **Port Already in Use**:
   ```bash
   # Find process using port 5000
   lsof -i :5000
   # Kill the process or use different port
   docker-compose up --build -p 5001:5000
   ```

2. **Permission Issues**:
   ```bash
   # Fix static directory permissions
   sudo chown -R $USER:$USER static/
   chmod -R 755 static/
   ```

3. **Model Files Missing**:
   ```bash
   # Ensure model files are present
   ls -la models/
   # Should contain: simple_nn_model.pth, feature_scaler.joblib
   ```

4. **Memory Issues**:
   ```bash
   # Increase Docker memory limit
   # Docker Desktop: Settings > Resources > Memory > 4GB+
   ```

### Container Logs

```bash
# View detailed logs
docker-compose logs --tail=100 -f

# View specific service logs
docker-compose logs qkd-razorpay-app
```

## 📋 Requirements

- Docker 20.10+
- Docker Compose 2.0+
- 4GB+ RAM (for quantum simulations)
- 2GB+ free disk space

## 🌐 Access Points

After successful deployment:

- **Main Application**: http://localhost:5000
- **QKD Simulation**: http://localhost:5000 (click "Start Simulation")
- **Presentation**: http://localhost:5000/presentation
- **API Documentation**: http://localhost:5000/api/simulations
- **Health Check**: http://localhost:5000/ (returns 200 OK)

## 🎯 Next Steps

1. Configure SSL certificates for HTTPS
2. Set up monitoring with Prometheus/Grafana
3. Implement log aggregation
4. Add automated backups
5. Configure CI/CD pipeline for updates

For more information, see the main [README.md](README.md) file. 