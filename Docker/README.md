# MXTSessions Generator - Docker Setup

This guide will help you containerize and run the MXTSessions Generator using Docker.

## 🚀 Quick Start

### Prerequisites
- Docker installed on your system
- Docker Compose (usually comes with Docker Desktop)

### Option 1: Using Docker Compose (Recommended)
```bash
# Clone the repository
git clone https://github.com/m3hr4nn/mxtsessions-generator.git
cd mxtsessions-generator/Docker

# Build and run with Docker Compose
docker-compose up --build
```

The application will be available at `http://localhost:5000`

### Option 2: Using Docker Commands

#### Development Build
```bash
# Build the image
docker build -t mxtsessions-generator:dev .

# Run the container
docker run -p 5000:5000 mxtsessions-generator:dev
```

#### Production Build
```bash
# Build production image
docker build -f Dockerfile-Gunicorn -t mxtsessions-generator:prod .

# Run the container
docker run -p 5000:5000 mxtsessions-generator:prod
```

### Option 3: Using Build Script
```bash
# Make the script executable
chmod +x build.sh

# Build development image
./build.sh dev

# Build production image
./build.sh prod

# Build both
./build.sh both
```

## 📁 File Structure

```
mxtsessions-generator/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── Dockerfile            # Development Dockerfile
├── Dockerfile-Gunicorn       # Production Dockerfile (with Gunicorn)
├── docker-compose.yml    # Docker Compose configuration
├── .dockerignore         # Docker ignore file
├── build.sh             # Build script
└── temp/                # Temporary files directory (auto-created)
```

## 🔧 Configuration

### Environment Variables
- `PORT`: Port to run the application (default: 5000)
- `FLASK_ENV`: Flask environment (development/production)

### Docker Compose Override
Create a `docker-compose.override.yml` file for custom configurations:

```yaml
version: '3.8'
services:
  mxtsessions-generator:
    ports:
      - "8080:5000"  # Change port
    environment:
      - FLASK_ENV=development
      - PORT=5000
```

## 🐳 Docker Images

### Development Image
- Uses Flask development server
- Suitable for testing and development
- Hot reload disabled in container

### Production Image
- Uses Gunicorn WSGI server
- 4 worker processes
- Optimized for production workloads
- Health checks enabled

## 📊 Health Checks

Both images include health checks that monitor the `/health` endpoint:
- **Interval**: 30 seconds
- **Timeout**: 30 seconds (10s for compose)
- **Retries**: 3
- **Start Period**: 5 seconds (40s for compose)

## 🛠️ Usage

### API Endpoints

1. **Home**: `GET /`
   - Returns API information and available endpoints

2. **Health Check**: `GET /health`
   - Returns application health status

3. **Generate Sessions**: `POST /generate`
   - Upload Excel file and generate MobaXterm sessions
   - Parameters:
     - `file`: Excel file (.xlsx)
     - `passwordFormat`: 'plain' or 'encrypted'
     - `encryptionKey`: Master password (required if encrypted)

### Example Usage with curl

```bash
# Health check
curl http://localhost:5000/health

# Generate sessions (plain passwords)
curl -X POST \
  -F "file=@servers.xlsx" \
  -F "passwordFormat=plain" \
  http://localhost:5000/generate \
  --output sessions.mxtsessions

# Generate sessions (encrypted passwords)
curl -X POST \
  -F "file=@servers.xlsx" \
  -F "passwordFormat=encrypted" \
  -F "encryptionKey=mypassword" \
  http://localhost:5000/generate \
  --output sessions_encrypted.mxtsessions
```

## 🔍 Monitoring and Logs

### View logs
```bash
# With Docker Compose
docker-compose logs -f

# With Docker run
docker logs -f <container_name>
```

### Container status
```bash
# Check container health
docker ps

# Inspect container
docker inspect mxtsessions-generator
```

## 🧹 Cleanup

### Stop and remove containers
```bash
# With Docker Compose
docker-compose down

# Remove images
docker-compose down --rmi all

# Remove volumes
docker-compose down --volumes
```

### Manual cleanup
```bash
# Stop container
docker stop mxtsessions-generator

# Remove container
docker rm mxtsessions-generator

# Remove image
docker rmi mxtsessions-generator:latest
```

## 🚨 Troubleshooting

### Common Issues

1. **Port already in use**
   ```bash
   # Change port in docker-compose.yml or use different port
   docker run -p 8080:5000 mxtsessions-generator:dev
   ```

2. **Permission denied**
   ```bash
   # Make build script executable
   chmod +x build.sh
   ```

3. **Docker not running**
   ```bash
   # Start Docker service
   sudo systemctl start docker  # Linux
   # Or start Docker Desktop
   ```

4. **Out of space**
   ```bash
   # Clean up Docker
   docker system prune -a
   ```

### Debug Mode

Run with debug output:
```bash
docker run -p 5000:5000 -e FLASK_ENV=development mxtsessions-generator:dev
```

## 📋 Excel File Requirements

Your Excel file must contain these columns:
- **Hostname**: Server hostname
- **IP**: IP address
- **user**: Username
- **password**: Password

## 🔐 Security Notes

- Passwords are processed in memory only
- Temporary files are automatically cleaned up
- Container runs as non-root user
- No persistent storage of sensitive data

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch
3. Make changes
4. Test with Docker
5. Submit a pull request

---

For more information, visit the [GitHub repository](https://github.com/m3hr4nn/mxtsessions-generator/).
