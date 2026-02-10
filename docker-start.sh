#!/bin/bash

# Quick Docker Start Script

echo ""
echo "🐳 Musicly Backend - Docker Quick Start"
echo "========================================"
echo ""

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running!"
    echo ""
    echo "Please start Docker and try again."
    echo ""
    exit 1
fi

echo "✅ Docker is running"
echo ""

# Check if .env file exists
if [ ! -f .env ]; then
    echo "⚠️  .env file not found!"
    echo ""
    echo "Creating .env from .env.example..."
    cp .env.example .env
    echo ""
    echo "⚠️  IMPORTANT: Edit .env file and add your Firebase credentials!"
    echo ""
    exit 1
fi

echo "✅ .env file found"
echo ""

# Ask which mode
echo "Choose mode:"
echo "  1. Production (optimized)"
echo "  2. Development (hot reload + Redis Commander)"
echo ""
read -p "Enter choice (1 or 2): " MODE

if [ "$MODE" == "2" ]; then
    echo ""
    echo "🚀 Starting in DEVELOPMENT mode..."
    echo ""
    docker-compose -f docker-compose.dev.yml up -d
    
    if [ $? -eq 0 ]; then
        echo ""
        echo "✅ Services started successfully!"
        echo ""
        echo "📍 Access points:"
        echo "   - Backend API: http://localhost:8000"
        echo "   - API Docs: http://localhost:8000/docs"
        echo "   - Redis Commander: http://localhost:8081"
        echo ""
        echo "📋 Useful commands:"
        echo "   - View logs: docker-compose -f docker-compose.dev.yml logs -f"
        echo "   - Stop: docker-compose -f docker-compose.dev.yml down"
        echo ""
    fi
else
    echo ""
    echo "🚀 Starting in PRODUCTION mode..."
    echo ""
    docker-compose up -d
    
    if [ $? -eq 0 ]; then
        echo ""
        echo "✅ Services started successfully!"
        echo ""
        echo "📍 Access points:"
        echo "   - Backend API: http://localhost:8000"
        echo "   - API Docs: http://localhost:8000/docs"
        echo ""
        echo "📋 Useful commands:"
        echo "   - View logs: docker-compose logs -f"
        echo "   - Stop: docker-compose down"
        echo ""
    fi
fi

echo "🧪 Testing backend..."
sleep 5
curl -s http://localhost:8000/health > /dev/null

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Backend is healthy!"
else
    echo ""
    echo "⚠️  Backend not responding yet. Check logs:"
    echo "   docker-compose logs -f backend"
fi

echo ""
