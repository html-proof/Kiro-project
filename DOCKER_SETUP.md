# 🐳 Docker Setup Guide

Complete guide to run Musicly Backend with Docker.

---

## 📋 What's Included

- **Dockerfile** - Production-ready multi-stage build
- **docker-compose.yml** - Production deployment
- **docker-compose.dev.yml** - Development with hot reload
- **.dockerignore** - Optimized build context

---

## 🚀 Quick Start (2 Minutes)

### Option 1: Production Mode

```bash
# 1. Make sure .env file exists with Firebase credentials
cp .env.example .env
# Edit .env with your Firebase credentials

# 2. Start services
docker-compose up -d

# 3. Check logs
docker-compose logs -f backend

# 4. Test
curl http://localhost:8000/health
```

### Option 2: Development Mode (with hot reload)

```bash
# 1. Make sure .env file exists
cp .env.example .env
# Edit .env with your Firebase credentials

# 2. Start services
docker-compose -f docker-compose.dev.yml up -d

# 3. Check logs
docker-compose -f docker-compose.dev.yml logs -f backend

# 4. Access services
# - Backend: http://localhost:8000
# - API Docs: http://localhost:8000/docs
# - Redis Commander: http://localhost:8081
```

---

## 📦 What Gets Deployed

### Services

1. **Backend (musicly-backend)**
   - FastAPI application
   - Port: 8000
   - Auto-restart enabled
   - Health checks configured

2. **Redis (musicly-redis)**
   - Redis 7 Alpine
   - Port: 6379
   - Persistent storage
   - Memory limit: 256MB
   - LRU eviction policy

3. **Redis Commander (dev only)**
   - Redis GUI
   - Port: 8081
   - View cache data

---

## 🔧 Docker Commands

### Build & Start

```bash
# Build images
docker-compose build

# Start services (detached)
docker-compose up -d

# Start services (with logs)
docker-compose up

# Start specific service
docker-compose up backend
```

### Stop & Remove

```bash
# Stop services
docker-compose stop

# Stop and remove containers
docker-compose down

# Stop and remove containers + volumes
docker-compose down -v
```

### Logs & Monitoring

```bash
# View logs (all services)
docker-compose logs

# Follow logs
docker-compose logs -f

# View backend logs only
docker-compose logs -f backend

# View Redis logs
docker-compose logs -f redis
```

### Execute Commands

```bash
# Access backend shell
docker-compose exec backend bash

# Access Redis CLI
docker-compose exec redis redis-cli

# Run Python command
docker-compose exec backend python -c "print('Hello')"

# Check Redis cache
docker-compose exec redis redis-cli KEYS "*"
```

### Health Checks

```bash
# Check service status
docker-compose ps

# Check backend health
curl http://localhost:8000/health

# Check Redis health
docker-compose exec redis redis-cli ping
```

---

## 🔐 Environment Variables

### Required Variables

Create `.env` file:

```env
# Firebase credentials (required)
FIREBASE_SERVICE_ACCOUNT_JSON={"type":"service_account",...}

# Redis URL (auto-configured in Docker)
REDIS_URL=redis://redis:6379

# CORS origins
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173

# Environment
APP_ENV=development
```

### Docker Compose Variables

```bash
# Set environment
export APP_ENV=production

# Set CORS origins
export ALLOWED_ORIGINS=https://yourdomain.com

# Start with custom env
docker-compose up -d
```

---

## 🏗️ Dockerfile Explained

### Multi-Stage Build

**Stage 1: Builder**
- Installs build dependencies
- Compiles Python packages
- Creates optimized wheel files

**Stage 2: Runtime**
- Minimal base image
- Only runtime dependencies
- Copies compiled packages
- Smaller final image

### Image Size

- **Builder stage:** ~800MB
- **Final image:** ~400MB
- **Optimized:** No build tools in production

### Features

- ✅ Python 3.11 slim base
- ✅ FFmpeg for media processing
- ✅ Health checks
- ✅ Non-root user (optional)
- ✅ Optimized layers
- ✅ Security best practices

---

## 🔄 Development Workflow

### Hot Reload Setup

```bash
# Start dev environment
docker-compose -f docker-compose.dev.yml up -d

# Edit code in ./app directory
# Changes auto-reload in container

# View logs
docker-compose -f docker-compose.dev.yml logs -f backend
```

### Redis Commander

Access at: http://localhost:8081

Features:
- View all keys
- Inspect cache data
- Delete keys
- Monitor memory

---

## 🚀 Production Deployment

### Build Production Image

```bash
# Build optimized image
docker-compose build --no-cache

# Tag for registry
docker tag musicly-backend:latest your-registry/musicly-backend:v1.0.0

# Push to registry
docker push your-registry/musicly-backend:v1.0.0
```

### Deploy to Server

```bash
# On production server
docker-compose -f docker-compose.yml up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f
```

### Environment Variables (Production)

```bash
# Set production env vars
export FIREBASE_SERVICE_ACCOUNT_JSON='{"type":"service_account",...}'
export REDIS_URL=redis://redis:6379
export ALLOWED_ORIGINS=https://yourdomain.com
export APP_ENV=production

# Deploy
docker-compose up -d
```

---

## 📊 Resource Limits

### Default Limits

```yaml
# Backend
- Memory: No limit (set in production)
- CPU: No limit (set in production)

# Redis
- Memory: 256MB (configured)
- Eviction: allkeys-lru
```

### Set Custom Limits

Edit `docker-compose.yml`:

```yaml
services:
  backend:
    deploy:
      resources:
        limits:
          cpus: '1.0'
          memory: 1G
        reservations:
          cpus: '0.5'
          memory: 512M
```

---

## 🔍 Troubleshooting

### Issue: Container won't start

```bash
# Check logs
docker-compose logs backend

# Check if Redis is healthy
docker-compose ps

# Restart services
docker-compose restart
```

### Issue: "Connection refused to Redis"

```bash
# Check Redis is running
docker-compose ps redis

# Check Redis health
docker-compose exec redis redis-cli ping

# Restart Redis
docker-compose restart redis
```

### Issue: "Firebase initialization failed"

```bash
# Check environment variables
docker-compose exec backend env | grep FIREBASE

# Verify .env file exists
cat .env

# Restart backend
docker-compose restart backend
```

### Issue: Port already in use

```bash
# Change port in docker-compose.yml
ports:
  - "8001:8000"  # Use 8001 instead

# Or stop conflicting service
docker ps
docker stop <container_id>
```

### Issue: Out of disk space

```bash
# Clean up unused images
docker system prune -a

# Remove unused volumes
docker volume prune

# Check disk usage
docker system df
```

---

## 🧪 Testing in Docker

### Run Tests

```bash
# Run test script
docker-compose exec backend python test_api.py

# Run setup verification
docker-compose exec backend python test_setup.py

# Test specific endpoint
docker-compose exec backend curl http://localhost:8000/health
```

### Interactive Testing

```bash
# Access container shell
docker-compose exec backend bash

# Inside container
python test_api.py
curl http://localhost:8000/search?q=test
redis-cli -h redis ping
```

---

## 📈 Monitoring

### Container Stats

```bash
# Real-time stats
docker stats

# Specific container
docker stats musicly-backend

# One-time stats
docker stats --no-stream
```

### Health Checks

```bash
# Check health status
docker-compose ps

# Manual health check
curl http://localhost:8000/health

# Redis health
docker-compose exec redis redis-cli ping
```

### Logs

```bash
# All logs
docker-compose logs

# Last 100 lines
docker-compose logs --tail=100

# Follow logs
docker-compose logs -f

# Specific service
docker-compose logs -f backend
```

---

## 🔒 Security Best Practices

### ✅ DO:

1. **Use .env for secrets**
   ```bash
   # Never commit .env
   echo ".env" >> .gitignore
   ```

2. **Keep images updated**
   ```bash
   docker-compose pull
   docker-compose up -d
   ```

3. **Use specific versions**
   ```yaml
   image: redis:7-alpine  # Not 'latest'
   ```

4. **Limit resources**
   ```yaml
   deploy:
     resources:
       limits:
         memory: 1G
   ```

### ❌ DON'T:

1. **Don't run as root** (add in Dockerfile if needed)
2. **Don't expose unnecessary ports**
3. **Don't use test mode in production**
4. **Don't commit secrets**

---

## 🌐 Networking

### Container Communication

```bash
# Backend connects to Redis
REDIS_URL=redis://redis:6379

# Containers use service names
# backend -> redis (automatic DNS)
```

### External Access

```bash
# Backend: http://localhost:8000
# Redis: localhost:6379
# Redis Commander: http://localhost:8081 (dev only)
```

### Custom Network

```yaml
networks:
  musicly-network:
    driver: bridge
    ipam:
      config:
        - subnet: 172.28.0.0/16
```

---

## 📦 Volumes

### Persistent Data

```bash
# List volumes
docker volume ls

# Inspect volume
docker volume inspect musicly-backend_redis-data

# Backup volume
docker run --rm -v musicly-backend_redis-data:/data -v $(pwd):/backup alpine tar czf /backup/redis-backup.tar.gz /data

# Restore volume
docker run --rm -v musicly-backend_redis-data:/data -v $(pwd):/backup alpine tar xzf /backup/redis-backup.tar.gz -C /
```

---

## 🚀 CI/CD Integration

### GitHub Actions Example

```yaml
name: Build and Push Docker Image

on:
  push:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Build image
        run: docker-compose build
      
      - name: Push to registry
        run: |
          docker tag musicly-backend:latest registry/musicly-backend:${{ github.sha }}
          docker push registry/musicly-backend:${{ github.sha }}
```

---

## 📚 Additional Resources

- **Docker Docs:** https://docs.docker.com
- **Docker Compose:** https://docs.docker.com/compose
- **Best Practices:** https://docs.docker.com/develop/dev-best-practices

---

## ✅ Quick Reference

```bash
# Start
docker-compose up -d

# Stop
docker-compose down

# Logs
docker-compose logs -f

# Restart
docker-compose restart

# Rebuild
docker-compose build --no-cache

# Clean
docker-compose down -v
docker system prune -a
```

---

**Your Docker setup is ready! 🐳**

Start with: `docker-compose up -d`
