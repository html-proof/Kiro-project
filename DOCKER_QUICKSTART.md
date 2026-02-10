# 🐳 Docker Quick Start

Get Musicly Backend running with Docker in 2 minutes!

---

## ✅ Prerequisites

- Docker Desktop installed
- Docker running
- `.env` file with Firebase credentials

---

## 🚀 Quick Start

### Option 1: Use Start Script (Easiest)

**Windows:**
```bash
docker-start.bat
```

**Linux/Mac:**
```bash
chmod +x docker-start.sh
./docker-start.sh
```

### Option 2: Manual Commands

**Production Mode:**
```bash
docker-compose up -d
```

**Development Mode (with hot reload):**
```bash
docker-compose -f docker-compose.dev.yml up -d
```

---

## 📍 Access Points

### Production Mode
- **Backend API:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs
- **Health Check:** http://localhost:8000/health

### Development Mode
- **Backend API:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs
- **Redis Commander:** http://localhost:8081

---

## 🔧 Common Commands

### Start Services
```bash
# Production
docker-compose up -d

# Development
docker-compose -f docker-compose.dev.yml up -d
```

### Stop Services
```bash
# Production
docker-compose down

# Development
docker-compose -f docker-compose.dev.yml down
```

### View Logs
```bash
# All services
docker-compose logs -f

# Backend only
docker-compose logs -f backend

# Redis only
docker-compose logs -f redis
```

### Restart Services
```bash
# All services
docker-compose restart

# Backend only
docker-compose restart backend
```

### Rebuild Images
```bash
# Rebuild and start
docker-compose up -d --build

# Force rebuild (no cache)
docker-compose build --no-cache
```

---

## 🧪 Testing

### Health Check
```bash
curl http://localhost:8000/health
```

### Search Music
```bash
curl "http://localhost:8000/search?q=arijit+singh"
```

### API Documentation
Open browser: http://localhost:8000/docs

---

## 🐛 Troubleshooting

### Services won't start
```bash
# Check Docker is running
docker info

# Check logs
docker-compose logs

# Restart Docker Desktop
```

### Port already in use
```bash
# Check what's using port 8000
netstat -ano | findstr :8000  # Windows
lsof -i :8000                 # Linux/Mac

# Change port in docker-compose.yml
ports:
  - "8001:8000"
```

### Backend not responding
```bash
# Check container status
docker-compose ps

# Check backend logs
docker-compose logs backend

# Restart backend
docker-compose restart backend
```

### Redis connection failed
```bash
# Check Redis is running
docker-compose ps redis

# Check Redis health
docker-compose exec redis redis-cli ping

# Restart Redis
docker-compose restart redis
```

---

## 📊 Monitoring

### Container Status
```bash
docker-compose ps
```

### Resource Usage
```bash
docker stats
```

### Redis Cache
```bash
# Access Redis CLI
docker-compose exec redis redis-cli

# View all keys
KEYS *

# Get specific key
GET search:test
```

---

## 🔄 Development Workflow

### With Hot Reload

1. **Start dev environment:**
   ```bash
   docker-compose -f docker-compose.dev.yml up -d
   ```

2. **Edit code in `./app` directory**
   - Changes auto-reload
   - No need to restart

3. **View logs:**
   ```bash
   docker-compose -f docker-compose.dev.yml logs -f backend
   ```

4. **Access Redis Commander:**
   - Open: http://localhost:8081
   - View cache data
   - Monitor Redis

---

## 🧹 Cleanup

### Stop and remove containers
```bash
docker-compose down
```

### Remove volumes (clears Redis data)
```bash
docker-compose down -v
```

### Remove images
```bash
docker-compose down --rmi all
```

### Full cleanup
```bash
docker-compose down -v --rmi all
docker system prune -a
```

---

## 📚 More Information

- **Full Docker Guide:** DOCKER_SETUP.md
- **Troubleshooting:** TROUBLESHOOTING.md
- **API Documentation:** API_DOCUMENTATION.md

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

# Status
docker-compose ps

# Rebuild
docker-compose up -d --build
```

---

**Your Docker setup is ready! 🐳**

Run: `docker-compose up -d` or use `docker-start.bat` / `docker-start.sh`
